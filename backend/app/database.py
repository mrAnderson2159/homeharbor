# backend/app/database.py
from getpass import getuser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import DATABASE_NAME, DATABASE_PORT

# Configura l'URL del database
DATABASE_URL = f"postgresql://{getuser()}@localhost:{DATABASE_PORT}/{DATABASE_NAME}"

# Crea l'engine per la connessione al database
engine = create_engine(DATABASE_URL)

# Configura la sessione
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea la classe base per i modelli
Base = declarative_base()


# Dependency per la connessione al database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
