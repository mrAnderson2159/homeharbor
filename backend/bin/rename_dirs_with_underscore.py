from os import walk, rename
from pathlib import Path


def rename_dirs_with_underscore(root: Path, exclude: list[str]):
    """
    Rinomina ricorsivamente le cartelle sotto `root` aggiungendo un `_`
    all'inizio del nome, escludendo quelle specificate in `exclude`.
    I file PDF non vengono rinominati.
    """
    for dirpath, dirnames, filenames in walk(root, topdown=False):
        current = Path(dirpath)

        # Se la cartella root è in `exclude`, salta tutto quel ramo
        if any(current.parts[:len(Path(e).parts)] == Path(e).parts for e in exclude):
            continue

        # Evita di rinominare se contiene solo PDF
        if all(f.endswith(".pdf") for f in filenames):
            continue

        # Se già ha "_" davanti, non serve rinominare
        if current.name.startswith("_"):
            continue

        # Rinomina
        new_path = current.parent / f"_{current.name}"
        try:
            rename(current, new_path)
            print(f"✔️  {current} -> {new_path}")
        except Exception as e:
            print(f"❌ Errore nel rinominare {current}: {e}")


if __name__ == "__main__":
    root = Path("/Volumes/working space/amministrazione")
    exclude = [
        ".Nuove Acquisizioni_backup",
        "Altro",
        "Nuove Acquisizioni"
        "Smistatore",  # nome esatto
    ]
    rename_dirs_with_underscore(root, exclude)
