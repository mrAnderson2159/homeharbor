import pytest
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.database import get_db

# Test di connessione al database
def test_database_connection():
    db: Session = next(get_db())  # Ottieni una sessione del database
    try:
        result = db.execute(text("SELECT 1"))  # Query di test
        row = result.fetchone()
        assert row is not None, "La query SELECT 1 non ha restituito risultati"
        assert row[0] == 1, "La query SELECT 1 non ha restituito il valore corretto"
    finally:
        db.close()
