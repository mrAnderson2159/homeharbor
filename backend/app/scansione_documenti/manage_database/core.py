# backend/app/scansione_documenti/manage_database/core.py
import pathlib
from os import PathLike, walk
from typing import Union

from sqlalchemy import select

from app.database import SessionLocal
from app.scansione_documenti import models
from app.scansione_documenti.manage_database.constants import EXCLUDED, ADMINISTRATION_PATH
from app.scansione_documenti.manage_database.tree import DB_Tree
from app.scansione_documenti.manage_database.utils import camel_to_snake, get_or_create, remove, sliced_admin

db = SessionLocal()


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

    for dirpath, _, _ in walk(path):
        if pathlib.Path(dirpath).name in excluded:
            continue

        parts = sliced_admin(pathlib.Path(dirpath).parts)
        level = len(parts)
        name = pathlib.Path(dirpath).name

        if 1 <= level <= 5:
            real_tree.add(DB_Tree.structure[level - 1], name)

    return real_tree


def get_needed_models() -> dict[str, ...]:
    structure = DB_Tree.structure

    return {
        camel_to_snake(model): getattr(models, model)
        for model in dir(models)
        if camel_to_snake(model) in structure
    }


def get_db_tree(needed_models: dict[str, ...]) -> DB_Tree:
    db_tree = DB_Tree()

    for model_name, model in needed_models.items():
        statement = select(model.name)
        query = db.execute(statement).scalars().all()

        for name in query:
            db_tree.add(model_name, name)

    return db_tree


def sync_db(path: Union[str, PathLike] = ADMINISTRATION_PATH):
    """
    Aggiorna il database con le cartelle presenti nel filesystem.
    """
    real_tree = get_real_tree(path)
    needed_models = get_needed_models()
    db_tree = get_db_tree(needed_models)

    to_add = real_tree - db_tree
    to_remove = db_tree - real_tree


    for key, values in to_add.items():
        for value in values:
            get_or_create(model=needed_models[key], filter_key='name', name=value)

    for key, values in to_remove.items():
        for value in values:
            remove(model=needed_models[key], filter_key='name', name=value)

    db.commit()
