# backend/app/paperless/routers/form.py
import re
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.functions import flat_singleton_list
from app.paperless.CRUD.document import get_all_documents
from app.paperless.CRUD.utility import get_all_utilities
from app.paperless.schema.form import FieldMeta
from app.paperless.CRUD.category import get_all_categories

router = APIRouter(prefix="/form", tags=["Form Metadata"])

@router.get("/structure", response_model=list[FieldMeta])
def get_structure_form_fields(db: Session = Depends(get_db)):
    db_categories = flat_singleton_list(get_all_categories(db, attrs=['name']))
    db_utilities = flat_singleton_list(get_all_utilities(db, attrs=['name']))
    db_documents = flat_singleton_list(get_all_documents(db, attrs=['name']))
    # filter out documents with no letters
    db_documents = [doc for doc in db_documents if re.search(r"[a-zA-Z]", doc)]
    # remove numbers, commas, colons, euro symbols, parentheses, hyphens, and periods
    db_documents = [re.sub(r"[\d,:€()\-.]", "", doc).strip() for doc in db_documents]
    # split by spaces
    db_documents = [doc.split(" ") for doc in db_documents]
    # flatten list and filter out words with less than 3 characters
    db_documents = [item for sublist in db_documents for item in sublist if len(item) > 2]
    # sort and remove duplicates
    db_documents = sorted(set(db_documents))
    return [
        FieldMeta(
            id="category_id",
            label="Categoria",
            type="text",
            required=True,
            autocomplete=db_categories
        ),
        FieldMeta(
            id="utility_id",
            label="Utenza",
            type="text",
            required=True,
            autocomplete=db_utilities
        ),
        FieldMeta(
            id="year_id",
            label="Anno",
            type="number",
            required=True,
            min=2000,
            max=datetime.now().year
        ),
        FieldMeta(
            id="document_type_id",
            label="Tipo documento",
            type="select",
            options=[
                {"label": "Default", "value": "default"},
                {"label": "Pagato", "value": "paid"},
                {"label": "Non pagato", "value": "not_paid"},
            ],
            required=True
        ),
        FieldMeta(
            id="document_id",
            label="Documento",
            type="text",
            required=True,
            autocomplete=db_documents
        )
    ]
