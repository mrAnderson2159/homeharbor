# backend/app/config.py
import os


def get_debug_mode():
    """
    Restituisce True se la modalità di debug è attiva.

    Legge la variabile d'ambiente DEBUG_MODE.
    Qualsiasi valore diverso da 'true' (case sensitive) sarà considerato False.

    Returns:
        bool: modalità di debug abilitata o meno.
    """
    mode = os.getenv("DEBUG_MODE", "false")
    return mode == "true"


def get_db_name():
    """
    Restituisce il nome del database da utilizzare.

    Legge la variabile d'ambiente DATABASE, con fallback su 'homeharbor'.

    Returns:
        str: nome del database.
    """
    return os.getenv("DATABASE", "homeharbor")


def get_db_port():
    """
    Restituisce la porta del database da utilizzare

    Legge la variabile d'ambiente DATABASE_PORT, con fallback su '15432'.

    Returns:
        str: porta del database.
    """
    return os.getenv("DATABASE_PORT", "15432")


def get_cors_origins():
    """
    Recupera l'indirizzo del frontend per l'header CORS.

    Legge la variabile FRONTEND_ADDRESS. Se non definita, restituisce stringa vuota.

    Returns:
        str: origine CORS autorizzata.
    """
    return os.getenv("FRONTEND_ADDRESS", "")


# Costanti globali utilizzabili in tutta l'app
DEBUG_MODE = get_debug_mode()
DATABASE_NAME = get_db_name()
DATABASE_PORT = get_db_port()
FRONTEND_ADDRESS = get_cors_origins()
