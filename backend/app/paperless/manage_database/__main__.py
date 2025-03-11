# backend/app/paperless/manage_database/__main__.py

# Script di sincronizzazione sicuro da rieseguire.
# Inserisce nuove voci trovate nel filesystem e rimuove quelle assenti.
# Viene richiamato automaticamente all'avvio di HomeHarbor (via startup task async).
from app.paperless.manage_database.core import db_init, sync_db

if __name__ == '__main__':
    db_init()
    sync_db()
