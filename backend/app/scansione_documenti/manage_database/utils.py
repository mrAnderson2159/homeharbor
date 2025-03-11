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

        print(f"🔍 {model.__name__}: ricerca per {filter_condition}")
        instance = db.query(model).filter_by(**filter_condition).first()

        attrs = None

        if instance:
            attrs = {k: v for k, v in vars(instance).items() if not k.startswith('_')}
            attrs = dict(sorted(attrs.items()))
            print(f"\t✅ Trovato: {attrs}")
        else:
            print("\t➕ Nessuna corrispondenza trovata.")

        return function(instance, *args, attrs=attrs, **kwargs)

    return wrapper


@crud
def get_or_create(instance, **kwargs):
    model = kwargs.pop('model')
    kwargs.pop('attrs')
    kwargs.pop('filter_key')  # evita conflitti con model(**kwargs)

    attrs = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())

    if instance:
        print()
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.flush()
        print(f"\t\t✅ Creato: {model.__name__}({attrs})\n")
        return instance


@crud
def remove(instance, **kwargs):
    attrs = kwargs.pop('attrs')
    model = kwargs.pop('model')

    attrs = ', '.join(f"{k}={repr(v)}" for k, v in attrs.items())

    if instance:
        db.delete(instance)
        db.flush()
        print(f"\t\t✅ Eliminato: {model.__name__}({attrs})\n")
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
