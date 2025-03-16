from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.paperless.CRUD.document import get_document_by_id, get_all_documents
from app.paperless.schema.response import DocumentSchema

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/{document_id}", response_model=DocumentSchema)
def _get_document_by_id(document_id: int, db: Session = Depends(get_db)):
    return get_document_by_id(document_id, db)


@router.get("/", response_model=list[DocumentSchema])
def _get_documents(db: Session = Depends(get_db)):
    return get_all_documents(db)

