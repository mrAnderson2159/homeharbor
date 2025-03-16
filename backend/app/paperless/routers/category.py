# backend/app/paperless/routers/category.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.paperless.CRUD.category import get_category_by_id, get_all_categories
from app.paperless.schema.response import CategorySchema
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategorySchema])
def _get_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get("/{category_id}", response_model=CategorySchema)
def _get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return get_category_by_id(category_id, db)
