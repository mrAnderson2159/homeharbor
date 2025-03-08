import sys
from setuptools import setup, find_packages

# Dipendenze comuni
common_requirements = [
    "numpy",
    "pillow",
    "opencv-python",
    "pyautogui"
]

# Dipendenze specifiche per OS
extra_requirements = {
    "win32": ["pyinsane2"],  # Windows
    "linux": ["sane"],  # Linux
    "darwin": [],  # macOS non ha bisogno di librerie Python aggiuntive per la scansione
}

# Rileva il sistema operativo e aggiunge le dipendenze corrispondenti
platform_key = sys.platform
if platform_key.startswith("win"):
    os_specific_requirements = extra_requirements.get("win32", [])
elif platform_key.startswith("linux"):
    os_specific_requirements = extra_requirements.get("linux", [])
elif platform_key.startswith("darwin"):
    os_specific_requirements = extra_requirements.get("darwin", [])
else:
    os_specific_requirements = []

# Unisce dipendenze comuni e specifiche
install_requires = common_requirements + os_specific_requirements

setup(
    name="homeharbor",
    version="1.0",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    install_requires=install_requires,
    include_package_data=True,  # ✅ Assicura che tutti i file siano inclusi
    options={
        "bdist_wheel": {"universal": True},  # ✅ Evita problemi con le wheel
        "egg_info": {"egg_base": "."},  # ✅ Imposta la directory corretta per evitare l'errore
    }
)