from sqlalchemy.orm import Session

from app.paperless.models import Document
from app.paperless.routers.functions import get_one, get_all

# ------------------------------ CREATE --------------------------------

# ------------------------------ READ --------------------------------

def get_document_by_id(document_id: int, db: Session, *, attrs: list[str] = None):
    return get_one(db, Document, document_id, attrs=attrs)


def get_all_documents(db: Session, *, attrs: list[str] = None):
    return get_all(db, Document, attrs=attrs)

# ------------------------------ UPDATE --------------------------------

# ------------------------------ DELETE --------------------------------