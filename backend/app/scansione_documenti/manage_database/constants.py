# backend/app/scansione_documenti/manage_database/constants.py
from os import PathLike
from typing import Union

EXCLUDED = [
    ".Nuove Acquisizioni_backup", "Altro", "Nuove Acquisizioni", "Smistatore",
    "amministrazione", "_amministrazione"
]

ADMINISTRATION_PATH: Union[str, PathLike] = '../../_amministrazione'  # '/Volumes/working space/amministrazione'
