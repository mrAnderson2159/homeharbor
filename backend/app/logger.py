# backend/app/logger.py
import logging

# Colori ANSI
RESET = "\x1b[0m"
GREY = "\x1b[38;21m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"
BOLD_RED = "\x1b[31;1m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"

# Formato colorato
_LOG_FORMAT = (
    f"{CYAN}FastAPI: {RESET}"
    f"{CYAN}%(asctime)s{RESET} - "
    f"{MAGENTA}%(name)s{RESET} - "
    f"{GREEN}%(levelname)s{RESET} - "
    f"{YELLOW}%(message)s{RESET}"
)

# Imposta il logger root
def configure_logging(debug: bool = False):
    if debug:
        logging.basicConfig(
            level=logging.INFO,
            format=_LOG_FORMAT,
        )

# Logger da usare nei moduli
logger = logging.getLogger("homeharbor")
