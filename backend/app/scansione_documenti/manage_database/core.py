# backend/app/scansione_documenti/manage_database/core.py
import pathlib
from os import PathLike, walk
from typing import Union, Literal, Callable

from sqlalchemy import select

from app.database import SessionLocal
from app.scansione_documenti import models
from app.scansione_documenti.manage_database.constants import EXCLUDED, ADMINISTRATION_PATH, MODELS_USING_INTEGER_NAME
from app.scansione_documenti.manage_database.tree import DB_Tree
from app.scansione_documenti.manage_database.utils import camel_to_snake, get_or_create, remove, sliced_admin, db


def db_init():
    for excluded in EXCLUDED:
        get_or_create(model=models.ExcludedPath, filter_key='path', path=excluded)

    db.commit()


def get_excluded_paths() -> list[str]:
    # 📘 scalars() - guida rapida
    #
    # Quando esegui una query con `session.execute(stmt)`, il risultato è una sequenza di righe (tuple).
    # Se stai selezionando una sola colonna, puoi usare `.scalars()` per ottenere direttamente i valori:
    #
    # ESEMPIO:
    # stmt = select(ExcludedPath.path)
    # paths = session.execute(stmt).scalars().all()
    # → restituisce una lista piatta di stringhe: ['path1', 'path2', ...]
    #
    # ✅ Usa `.scalars()` quando selezioni UNA sola colonna
    # ❌ NON usare `.scalars()` se stai selezionando più colonne o intere righe
    #
    # ┌───────────────────────────────────────────────┐
    # | QUERY SQL                          | SCALARS? |
    # ├───────────────────────────────────────────────┤
    # | SELECT path FROM excluded_paths    |   ✅     |
    # | SELECT id FROM users               |   ✅     |
    # | SELECT * FROM users                |   ❌     |
    # | SELECT id, username FROM users     |   ❌     |
    # └───────────────────────────────────────────────┘
    #
    # Puoi anche combinarlo con `.first()` o `.one()`:
    # username = session.execute(select(User.username).where(User.id == 1)).scalars().first()
    #
    # Ricorda:
    # → scalars = "dammi solo i valori"
    # → all = "mettili in lista"
    statement = select(models.ExcludedPath.path)
    return db.execute(statement).scalars().all()


def get_real_tree(path: Union[str, PathLike]) -> DB_Tree:
    excluded = get_excluded_paths()
    real_tree = DB_Tree()

    # print(f"Looking for {path} and is {path.exists()} that it exists")

    for dirpath, _, _ in walk(path):
        # print(dirpath)
        if pathlib.Path(dirpath).name in excluded:
            continue

        parts = sliced_admin(pathlib.Path(dirpath).parts)
        level = len(parts)
        name = pathlib.Path(dirpath).name

        # print(f"📁 {level=}, {name=}, {parts=}")

        if 1 <= level <= 5:
            real_tree.add(DB_Tree.structure[level - 1], name)
            # print(f"🌳 {real_tree}, DB_Tree.structure[level - 1] = {DB_Tree.structure[level - 1]}")
            if level == 5:
                real_tree.add('paths', str(pathlib.Path(*parts)))

    return real_tree


def get_needed_models() -> dict[str, ...]:
    structure = DB_Tree.structure

    return {
        camel_to_snake(model): getattr(models, model)
        for model in dir(models)
        if camel_to_snake(model) in structure
    }

def get_all_path_labels(return_type: Literal['query', 'PathLike', 'posix']) -> Union[
    list[tuple[str, str, str, str, str]],
    list[PathLike],
    list[str]
]:
    stmt = (
        select(
            models.Category.name,
            models.Utility.name,
            models.Year.name,
            models.DocumentType.name,
            models.Document.name
        )
        .join(models.Path.category_rel)
        .join(models.Path.utility_rel)
        .join(models.Path.year_rel)
        .join(models.Path.document_type_rel)
        .join(models.Path.document_rel)
    )

    result = db.execute(stmt).all()

    match return_type:
        case 'query':
            return result
        case 'PathLike':
            return [pathlib.Path(*map(str, parts)) for parts in result] # usiamo map(str, parts) per gli anni
        case 'posix':
            return [pathlib.Path(*map(str, parts)).as_posix() for parts in result]
        case _:
            raise ValueError("Tipo di ritorno non valido. Usa 'query', 'PathLike' o 'posix'.")


def get_db_tree(needed_models: dict[str, ...]) -> DB_Tree:
    db_tree = DB_Tree()

    for model_name, model in needed_models.items():
        statement = select(model.name)
        query = db.execute(statement).scalars().all()

        if model in MODELS_USING_INTEGER_NAME:
            query = [str(name) for name in query]

        for name in query:
            db_tree.add(model_name, name)

    db_tree.paths = set(get_all_path_labels('posix'))

    return db_tree


def process_posix_path(path: str) -> dict[str, str]:
    parts = pathlib.PurePosixPath(path).parts

    return {
        'category': parts[0],
        'utility': parts[1],
        'year': parts[2],
        'document_type': parts[3],
        'document': parts[4]
    }

def get_id_from_name(model: str, name: str) -> int:
    model_name = {
        'category': 'Category',
        'utility': 'Utility',
        'year': 'Year',
        'document_type': 'DocumentType',
        'document': 'Document'
    }[model]

    model = getattr(models, model_name)

    statement = select(model.id).where(model.name == name)
    return db.execute(statement).scalar()

def crud_path(path: str, function: Callable):
    kwargs = process_posix_path(path)
    filter_key = ', '.join(kwargs.keys())
    ids = {key: get_id_from_name(key, value) for key, value in kwargs.items()}

    return function(model=models.Path, filter_key=filter_key, **ids)


def sync_db(path: Union[str, PathLike] = ADMINISTRATION_PATH):
    """
    Aggiorna il database con le cartelle presenti nel filesystem.
    """
    real_tree = get_real_tree(path)
    # print(f"🌳 Real tree:\n{real_tree}")
    needed_models = get_needed_models()
    # print(f"🏗️ Needed models:\n{needed_models}")
    db_tree = get_db_tree(needed_models)
    # print(f"🏢 DB tree:\n{db_tree}")

    to_add = real_tree - db_tree
    to_remove = db_tree - real_tree
    # print(f"🌱 To add:\n{to_add}")
    # print(f"🔥 To remove:\n{to_remove}")

    for key, values in to_add.items():
        for value in values:
            if key == 'paths':
                crud_path(value, get_or_create)
            else:
                get_or_create(model=needed_models[key], filter_key='name', name=value)

    for key, values in to_remove.items():
        for value in values:
            if key == 'paths':
                crud_path(value, remove)
            else:
                remove(model=needed_models[key], filter_key='name', name=value)

    db.commit()
