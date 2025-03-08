# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configura l'URL del database
DATABASE_URL = f"postgresql://mr.anderson2159@localhost/homeharbor"

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
