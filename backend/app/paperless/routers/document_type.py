from fastapi import APIRouter
from app.paperless.schema.response import DocumentTypeSchema

router = APIRouter(prefix="/document_types", tags=["Document Types"])