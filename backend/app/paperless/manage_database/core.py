# backend/app/paperless/manage_database/core.py

"""
Modulo centrale per la gestione della sincronizzazione tra il file system
e il database di HomeHarbor.

Le principali responsabilità includono:
- Ottenere la struttura reale delle cartelle.
- Ottenere la struttura attualmente salvata nel database.
- Calcolare le differenze tra le due strutture.
- Applicare le modifiche necessarie al database.
"""

import pathlib
from os import PathLike, walk
from typing import Union, Literal, Callable

from sqlalchemy import select

from app.paperless import models
from app.paperless.manage_database.constants import EXCLUDED, MOCK_ADMINISTRATION_PATH, \
    MODELS_USING_INTEGER_NAME
from app.paperless.manage_database.tree import DB_Tree
from app.paperless.manage_database.utils import camel_to_snake, get_or_create, remove, sliced_admin, db


def db_init():
    """
    Inserisce nel database i percorsi da escludere definiti in `EXCLUDED`,
    se non già presenti. Questa operazione è idempotente.
    """
    for excluded in EXCLUDED:
        get_or_create(model=models.ExcludedPath, filter_key='path', path=excluded)

    db.commit()


def get_excluded_paths() -> list[str]:
    """
    Recupera tutti i path da escludere dal database, contenuti nella tabella `excluded_paths`.

    Returns:
        list[str]: elenco di percorsi da ignorare durante la scansione.
    """
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
    """
    Costruisce un oggetto `DB_Tree` rappresentante la struttura reale del file system,
    a partire dal percorso `path`. Esclude i path specificati in `EXCLUDED`.

    Args:
        path (str | PathLike): percorso della root di amministrazione.

    Returns:
        DB_Tree: struttura rilevata dal file system.
    """
    excluded = get_excluded_paths()
    real_tree = DB_Tree()

    for dirpath, _, _ in walk(path):
        # Ignora le directory il cui nome corrisponde a una voce esclusa
        if pathlib.Path(dirpath).name in excluded:
            continue

        # Estrae solo la parte del path dopo la cartella root di amministrazione
        # (es. '_amministrazione' in mock, 'amministrazione' in produzione)
        parts = sliced_admin(pathlib.Path(dirpath).parts)
        level = len(parts)
        name = pathlib.Path(dirpath).name

        if 1 <= level <= 5:
            # Aggiunge il nome alla struttura appropriata (category, utility, etc.)
            real_tree.add(DB_Tree.structure[level - 1], name)

            # Se siamo al quinto livello (documento), aggiungiamo il path completo
            if level == 5:
                real_tree.add('paths', str(pathlib.Path(*parts)))

    return real_tree


def get_needed_models() -> dict[str, ...]:
    """
    Ritorna un dizionario che mappa i nomi delle entità (in snake_case)
    ai relativi modelli SQLAlchemy nella struttura di `DB_Tree`.

    Returns:
        dict[str, ...]: mapping tra nome entità e modello.
    """
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
    """
    Recupera tutti i path presenti nella tabella `paths`, unendo le foreign key
    per ottenere i nomi leggibili delle entità (category, utility, year, ecc.).

    Args:
        return_type (str): può essere 'query', 'PathLike', o 'posix'

    Returns:
        list: elenco dei path nel formato specificato
    """

    # SQL equivalente alla seguente query ORM:
    #
    # SELECT c.name, u.name, y.name, dt.name, d.name
    # FROM paths p
    # JOIN categories c ON p.category = c.id
    # JOIN utilities u ON p.utility = u.id
    # JOIN years y ON p.year = y.id
    # JOIN document_types dt ON p.document_type = dt.id
    # JOIN documents d ON p.document = d.id

    stmt = (
        select(
            models.Category.name,
            models.Utility.name,
            models.Year.name,
            models.DocumentType.name,
            models.Document.name
        )
        # I join successivi collegano ciascuna FK della tabella `paths`
        # alla rispettiva tabella relazionale per ottenere i nomi umani (anziché gli id)
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
            # PathLike è utile per confronti con il file system
            return [pathlib.Path(*map(str, parts)) for parts in result]
        case 'posix':
            # formato stringa standardizzato (con '/' come separatore)
            return [pathlib.Path(*map(str, parts)).as_posix() for parts in result]
        case _:
            raise ValueError("Tipo di ritorno non valido. Usa 'query', 'PathLike' o 'posix'.")


def get_db_tree(needed_models: dict[str, ...]) -> DB_Tree:
    """
    Crea un `DB_Tree` basato sui dati attualmente presenti nel database,
    inclusi i path derivati da `get_all_path_labels`.

    Args:
        needed_models (dict): mapping tra nomi logici e modelli SQLAlchemy.

    Returns:
        DB_Tree: struttura corrente del database.
    """

    db_tree = DB_Tree()

    for model_name, model in needed_models.items():
        statement = select(model.name)
        query = db.execute(statement).scalars().all()

        # Alcuni modelli usano interi come nomi (es. Year) ma il DB_Tree
        # usa sempre stringhe, quindi convertiamo per coerenza
        if model in MODELS_USING_INTEGER_NAME:
            query = [str(name) for name in query]

        for name in query:
            db_tree.add(model_name, name)

    # I path completi (es. categoria/utenza/anno/...) vengono
    # aggiunti separatamente come stringhe posix
    db_tree.paths = set(get_all_path_labels('posix'))

    return db_tree


def process_posix_path(path: str) -> dict[str, str]:
    """
    Converte un percorso POSIX in un dizionario con le chiavi corrispondenti
    alle entità (category, utility, year, etc.).

    Args:
        path (str): percorso POSIX come stringa.

    Returns:
        dict[str, str]: dizionario con chiavi ed etichette.
    """

    parts = pathlib.PurePosixPath(path).parts

    return {
        'category': parts[0],
        'utility': parts[1],
        'year': parts[2],
        'document_type': parts[3],
        'document': parts[4]
    }


def get_id_from_name(model: str, name: str) -> int:
    """
    Data un'entità e il suo nome, restituisce l'ID corrispondente nel database.

    Args:
        model (str): nome dell'entità (es. 'category', 'utility', ...)
        name (str): nome dell'istanza da cercare

    Returns:
        int: ID del record corrispondente
    """

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
    """
    Wrapper per le operazioni `get_or_create` e `remove` relative ai path completi.

    Args:
        path (str): path POSIX da processare
        function (Callable): funzione da eseguire sul path (es. get_or_create o remove)

    Returns:
        Any: risultato della funzione chiamata
    """

    kwargs = process_posix_path(path)
    filter_key = ', '.join(kwargs.keys())
    ids = {key: get_id_from_name(key, value) for key, value in kwargs.items()}

    return function(model=models.Path, filter_key=filter_key, **ids)


def sync_db(path: Union[str, PathLike] = MOCK_ADMINISTRATION_PATH):
    """
    Esegue la sincronizzazione tra file system e database.

    - Identifica tutte le nuove entità da creare.
    - Identifica tutte le entità obsolete da eliminare.
    - Applica le modifiche tramite `get_or_create` e `remove`.

    Args:
        path (str | PathLike): percorso della root da scansionare. Di default `MOCK_ADMINISTRATION_PATH`.
    """

    # Costruisce l'albero reale analizzando il file system (directory presenti fisicamente)
    real_tree = get_real_tree(path)

    # Recupera i modelli SQLAlchemy rilevanti (category, utility, ecc.)
    needed_models = get_needed_models()

    # Costruisce l'albero virtuale a partire dal contenuto effettivo del database
    db_tree = get_db_tree(needed_models)

    # Determina quali entità sono presenti nel file system ma non nel database
    to_add = real_tree - db_tree

    # Determina quali entità sono nel database ma non più presenti nel file system
    to_remove = db_tree - real_tree

    # Aggiunge entità mancanti
    for key, values in to_add.items():
        for value in values:
            if key == 'paths':
                # I path richiedono una gestione speciale con ID, quindi usiamo `crud_path`
                crud_path(value, get_or_create)
            else:
                get_or_create(model=needed_models[key], filter_key='name', name=value)

    # Rimuove entità non più esistenti nel file system
    for key, values in to_remove.items():
        for value in values:
            if key == 'paths':
                crud_path(value, remove)
            else:
                remove(model=needed_models[key], filter_key='name', name=value)

    # Salva tutte le modifiche nel database
    db.commit()
