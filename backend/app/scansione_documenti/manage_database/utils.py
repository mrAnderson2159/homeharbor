# backend/app/scansione_documenti/manage_database/utils.py
import re
from functools import wraps

from app.database import SessionLocal

db = SessionLocal()


def crud(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        model = kwargs['model']
        filter_key = kwargs['filter_key']

        if not all([model, filter_key]):
            raise ValueError("Missing required keyword argument: 'model' or 'filter_key'")

        if filter_key == '*':
            filter_condition = kwargs
        else:
            keys = [key.strip() for key in filter_key.split(',')]
            filter_condition = {key: kwargs[key] for key in keys if key in kwargs}

        print(f"🔍 Ricerca: {model.__name__} - {filter_condition}")
        instance = db.query(model).filter_by(**filter_condition).first()
        print(f"istanza: {instance.__dict__ if instance else None}")
        return function(instance, *args, **kwargs)

    return wrapper


@crud
def get_or_create(instance, context_info=None, **kwargs):
    model = kwargs.pop('model')
    kwargs.pop('filter_key')  # evita conflitti con model(**kwargs)

    if instance:
        print(f"⚠️  Esiste già: {instance} - Context: {context_info}")
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.flush()
        db.refresh(instance)
        print(f"✅ Creato: {instance} - Context: {context_info}")
        return instance


@crud
def remove(instance, context_info=None, **kwargs):
    if instance:
        db.delete(instance)
        db.flush()
        print(f"✅ Eliminato: {instance} - Context: {context_info}")
        return instance


def sliced_admin(t: tuple[str, ...]) -> tuple[str, ...]:
    if '_amministrazione' not in t:
        raise ValueError("Path non contiene '_amministrazione'")

    index = t.index('_amministrazione')
    return t[index + 1:]


def camel_to_snake(name: str) -> str:
    """
    Converte una stringa CamelCase in snake_case.

    Esempio:
        CamelCase -> camel_case
        HTTPResponseCode -> http_response_code
    """
    # Inserisce un underscore tra lettere minuscole e maiuscole o tra lettere maiuscole seguite da minuscole
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
    return name.lower()
