# backend/app/scansione_documenti/manage_database/constants.py
from os import PathLike
from typing import Union
from pathlib import Path

from app.scansione_documenti.models import Year

def root_path() -> Path:
    path = Path(__file__).resolve()
    path_parts = path.parts
    try:
        index_root = path_parts.index('backend')
    except ValueError:
        raise RuntimeError("Impossibile trovare 'backend' nel percorso. Sei sicuro che il progetto sia strutturato correttamente?")

    return Path(*path_parts[:index_root + 1])


ROOT: Path = root_path()

EXCLUDED = [
    ".Nuove Acquisizioni_backup", "Altro", "Nuove Acquisizioni", "Smistatore",
    "amministrazione", "_amministrazione"
]

ADMINISTRATION_PATH: Union[str, PathLike] = ROOT / '_amministrazione'  # '/Volumes/working space/amministrazione'

# Alcuni modelli usano interi nel campo `name` (es. Year).
# Serve per allineare il tipo con i nomi delle cartelle (che sono sempre stringhe).
MODELS_USING_INTEGER_NAME = [Year]
