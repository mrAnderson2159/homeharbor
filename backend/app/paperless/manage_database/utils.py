"""
utils.py

Modulo di utilità per la gestione delle operazioni CRUD semplificate con logging dettagliato
e per la manipolazione dei path e dei nomi dei modelli.

Contiene:
- Un decoratore `crud` per centralizzare la logica di ricerca e logging.
- Funzioni `get_or_create` e `remove` per interagire col database evitando duplicazioni.
- Funzioni di supporto per conversioni tra nomi e manipolazione dei path dell'applicazione.

Questo modulo è usato principalmente durante la sincronizzazione tra filesystem e database.
"""

import re
from functools import wraps

from app.database import SessionLocal

db = SessionLocal()

def crud(function):
    """
    Decoratore per operazioni CRUD che intercetta e gestisce la ricerca
    di una riga nel database prima di eseguire la funzione.

    Richiede che la funzione decorata accetti `model`, `filter_key`
    e gli argomenti necessari al filtro come keyword arguments.

    Aggiunge un logging dettagliato dell'operazione e passa l'istanza trovata
    (o None) alla funzione decorata, insieme ad `attrs`, un dizionario con gli
    attributi rilevanti per il logging.

    Esempio:
        @crud
        def get_or_create(instance, **kwargs):
            ...
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        # Recupera il modello e la chiave di filtro dagli argomenti passati
        model = kwargs['model']
        filter_key = kwargs['filter_key']

        # Verifica che entrambi siano presenti, altrimenti lancia un errore
        if not all([model, filter_key]):
            raise ValueError("Missing required keyword argument: 'model' or 'filter_key'")

        # Se il filtro è un wildcard '*', usa direttamente tutti i kwargs come condizioni
        if filter_key == '*':
            filter_condition = kwargs
        else:
            # Altrimenti, spezza la stringa filter_key per ottenere le chiavi (anche multiple, separate da virgola)
            # e costruisce il dizionario per il filtro usando solo i kwargs corrispondenti
            keys = [key.strip() for key in filter_key.split(',')]
            filter_condition = {key: kwargs[key] for key in keys if key in kwargs}

        # Esegui la query per cercare se esiste già un'istanza corrispondente
        print(f"🔍 {model.__name__}: ricerca per {filter_condition}")
        instance = db.query(model).filter_by(**filter_condition).first()

        attrs = None
        if instance:
            # Se trovata, costruisce un dizionario `attrs` con gli attributi pubblici dell'istanza
            # (escludendo quelli che iniziano con '_') e li ordina per leggibilità
            attrs = {k: v for k, v in vars(instance).items() if not k.startswith('_')}
            attrs = dict(sorted(attrs.items()))
            print(f"\t✅ Trovato: {attrs}")
        else:
            print("\t➕ Nessuna corrispondenza trovata.")

        # Chiama la funzione decorata, passandole l'istanza trovata (o None),
        # insieme agli argomenti originali, arricchiti con `attrs`
        return function(instance, *args, attrs=attrs, **kwargs)

    return wrapper


@crud
def get_or_create(instance, **kwargs):
    """
    Restituisce l'istanza se esiste già, altrimenti la crea nel database.

    Deve essere usata con il decoratore `@crud`.

    Argomenti richiesti in kwargs:
    - model: il modello SQLAlchemy
    - filter_key: le chiavi usate per filtrare
    - tutti gli altri campi necessari per creare l'oggetto
    """
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
    """
    Elimina un'istanza esistente dal database, se trovata.

    Deve essere usata con il decoratore `@crud`.

    Argomenti richiesti in kwargs:
    - model: il modello SQLAlchemy
    - filter_key: le chiavi usate per filtrare
    """
    attrs = kwargs.pop('attrs')
    model = kwargs.pop('model')

    attrs = ', '.join(f"{k}={repr(v)}" for k, v in attrs.items())

    if instance:
        db.delete(instance)
        db.flush()
        print(f"\t\t✅ Eliminato: {model.__name__}({attrs})\n")
        return instance


def sliced_admin(t: tuple[str, ...]) -> tuple[str, ...]:
    """
    Ritorna la parte del path *dopo* '_amministrazione'.

    Usata per estrarre la struttura logica della cartella (es. categoria, utenza, ecc.)
    da un path assoluto.

    Esempio:
        sliced_admin(('Users', 'vale', '_amministrazione', 'Banca', 'Deutsche'))
        → ('Banca', 'Deutsche')
    """
    if '_amministrazione' not in t:
        raise ValueError("Path non contiene '_amministrazione'")

    index = t.index('_amministrazione')
    return t[index + 1:]


def camel_to_snake(name: str, reverse: bool = False, pascal: bool = False) -> str:
    """
    Converte un nome CamelCase in snake_case e viceversa.

    Argomenti:
    - name: stringa da convertire.
    - reverse: se True, converte da snake_case a camelCase.
    - pascal: se True con reverse=True, restituisce PascalCase.

    Esempi:
        camel_to_snake("DocumentType") → 'document_type'
        camel_to_snake("document_type", reverse=True) → 'documentType'
        camel_to_snake("document_type", reverse=True, pascal=True) → 'DocumentType'
    """
    if reverse:
        name = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)
        return name.capitalize() if pascal else name
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
    return name.lower()
