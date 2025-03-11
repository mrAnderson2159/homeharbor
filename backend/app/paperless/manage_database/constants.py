# backend/app/paperless/manage_database/constants.py

"""
Costanti globali per il modulo di gestione del database.

Questo file contiene variabili condivise come percorsi, cartelle da escludere
dalla scansione e modelli speciali da trattare con attenzione.

Contenuto principale:
- Percorsi assoluti alla radice del progetto e alla directory amministrativa.
- Lista di cartelle da ignorare durante la scansione.
- Modelli che usano numeri interi come nome (es. `Year`), da convertire a stringa
  per confronto coerente col file system.
"""

from os import PathLike
from typing import Union
from pathlib import Path

from app.paperless.models import Year


def _root_path() -> Path:
    """
    Restituisce il percorso assoluto del progetto fino alla cartella 'backend'.

    Questo serve per costruire percorsi dinamici e portabili,
    evitando hardcoding nei path assoluti del filesystem.
    """
    path = Path(__file__).resolve()
    path_parts = path.parts

    try:
        index_root = path_parts.index('backend')
    except ValueError:
        raise RuntimeError(
            "Impossibile trovare 'backend' nel percorso. "
            "Sei sicuro che il progetto sia strutturato correttamente?"
        )

    return Path(*path_parts[:index_root + 1])


# Percorso assoluto al progetto (fino alla cartella 'backend')
ROOT: Path = _root_path()


# Cartelle da escludere durante la scansione del filesystem.
# Vengono ignorate completamente da get_real_tree().
EXCLUDED = [
    ".Nuove Acquisizioni_backup", "Altro", "Nuove Acquisizioni", "Smistatore",
    "amministrazione", "_amministrazione"
]


# MOCK_ADMINISTRATION_PATH è usato in fase di sviluppo o test locale.
MOCK_ADMINISTRATION_PATH: Union[str, PathLike] = ROOT / '_amministrazione'

# ADMINISTRATION_PATH è il percorso reale della directory che contiene le cartelle
# da mappare e sincronizzare nel database. Va usato in produzione.
ADMINISTRATION_PATH: Union[str, PathLike] = '/Volumes/working space/amministrazione'


# Alcuni modelli (come Year) usano un campo `name` di tipo intero.
# Dato che i nomi delle cartelle nel filesystem sono stringhe,
# questo serve per effettuare confronti e casting coerenti.
MODELS_USING_INTEGER_NAME = [Year]
