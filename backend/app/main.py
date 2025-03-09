# backend/app/main.py
import logging
from fastapi import FastAPI, Request, HTTPException
from app.config import DEBUG_MODE, DATABASE_NAME, FRONTEND_ADDRESS
from fastapi.middleware.cors import CORSMiddleware


# Definisce i colori per ciascuna parte del messaggio
RESET = "\x1b[0m"
GREY = "\x1b[38;21m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"
BOLD_RED = "\x1b[31;1m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"

# Definisce il formato del log, aggiungendo colori a ciascuna sezione
log_format = (
    f"{CYAN}FastAPI: {RESET}"
    f"{CYAN}%(asctime)s{RESET} - "
    f"{MAGENTA}%(name)s{RESET} - "
    f"{GREEN}%(levelname)s{RESET} - "
    f"{YELLOW}%(message)s{RESET}"
)
print()

if DEBUG_MODE:
    # Configura il logging con il formatter colorato
    logging.basicConfig(
        level=logging.INFO,  # Livello di logging impostato a INFO
        format=log_format,  # Formato del log
    )

logger = logging.getLogger(__name__)
logger.info("Server starting...")

app = FastAPI()

# Lista dei frontend consentiti (inizialmente vuota)
allowed_origins = [FRONTEND_ADDRESS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS abilitato per gli indirizzi: {allowed_origins}{RESET}")

@app.middleware("http")
async def block_unauthorized_requests(request: Request, call_next):
    # logger.info(f"Richiesta in arrivo: {request.client}")
    origin = request.headers.get("origin")  # Prende l'origin dalla richiesta
    if origin and origin not in allowed_origins:
        raise HTTPException(status_code=403, detail="Forbidden: Origin not allowed")
    return await call_next(request)


@app.get("/")
def read_root():
    return {"message": "FastAPI è attivo!"}

