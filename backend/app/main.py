# backend/app/main.py

"""
Punto di ingresso principale per l'app FastAPI.

- Configura logging colorato in modalità sviluppo.
- Imposta il middleware CORS.
- Blocca le richieste HTTP con origin non autorizzato.
- Espone la rotta di test '/'.
"""

from app.logger import configure_logging, logger
from fastapi import FastAPI, Request, HTTPException
from app.config import DEBUG_MODE, DATABASE_NAME, FRONTEND_ADDRESS
from fastapi.middleware.cors import CORSMiddleware

configure_logging(DEBUG_MODE)

logger.info("Server starting...")

app = FastAPI()

logger.info("Server started.")
logger.info(f"Modalità debug: {DEBUG_MODE}")
logger.info(f"Database: {DATABASE_NAME}")

# Lista dei frontend consentiti (inizialmente vuota)
allowed_origins = [FRONTEND_ADDRESS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS abilitato per gli indirizzi: {allowed_origins}")

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

