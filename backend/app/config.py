# backend/app/config.py
import os

def get_debug_mode():
    mode = os.getenv("DEBUG_MODE", "false")
    return mode == "true"

def get_db_name():
    return os.getenv("DATABASE", "homeharbor")

def get_cors_origins():
    return os.getenv("FRONTEND_ADDRESS", "")

DEBUG_MODE = get_debug_mode()
DATABASE_NAME = get_db_name()
FRONTEND_ADDRESS = get_cors_origins()
