# backend/app/paperless/routers/functions.py
from fastapi import HTTPException
from sqlalchemy.orm import Session  # Importa la sessione per interagire con il database
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.database import Base


def try_except(func):
    """
    Decoratore per gestire le eccezioni nei metodi di questo modulo,
    distinguendo tra errori server-side e client-side.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            # Passa eccezioni HTTPException esistenti senza modificarle
            print(e)
            raise e
        except Exception as e:
            # Per altre eccezioni, restituisce un errore generico server-side
            print(e)
            raise HTTPException(status_code=500, detail=f"Errore interno: {str(e)}")
    return wrapper


def select(model, attributes: list[str]) -> list[InstrumentedAttribute]:
    """
    Filtra gli attributi di un modello in base a una lista di nomi.

    :param model: Modello da cui filtrare gli attributi.
    :param attributes: Lista di nomi degli attributi da mantenere.
    :return: Lista di attributi del modello.
    """
    if not attributes or len(attributes) == 0:
        return [model]

    valid_attrs = {attr for attr in dir(model) if not attr.startswith("_")}
    invalid = [attr for attr in attributes if attr not in valid_attrs]
    if invalid:
        raise ValueError(f"Attributi non validi per {model.__name__}: {invalid}")

    return [getattr(model, attr) for attr in attributes]




@try_except
def get_one(db: Session, model: type[Base], obj_id: int, *, attrs: list[str] = None) -> Base:
    """
    Recupera un oggetto di un modello dal database.

    :param db: Sessione del database.
    :param model: Modello da cui recuperare l'oggetto.
    :param obj_id: ID dell'oggetto da recuperare.
    :return: Oggetto del modello.
    """
    query = db.query(*select(model, attrs)).filter(model.id == obj_id).first()
    if not query:
        raise HTTPException(status_code=404, detail=f'"{model.__name__}" non trovato')
    return query


@try_except
def get_all(db: Session, model: type[Base], *, attrs: list[str] = None) -> list[Base]:
    """
    Recupera tutti gli oggetti di un modello dal database.

    :param db: Sessione del database.
    :param model: Modello da cui recuperare gli oggetti.
    :return: Lista di oggetti del modello.
    """
    query = db.query(*select(model, attrs)).order_by(model.id).all()
    if not query:
        raise HTTPException(status_code=404, detail=f'"{model.__name__}" non trovato')
    return query
