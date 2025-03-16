# backend/app/paperless/CRUD/category.py
from sqlalchemy.orm import Session

from app.paperless.models import Category
from app.paperless.routers.functions import get_one, get_all

# ------------------------------ CREATE --------------------------------

# ------------------------------ READ --------------------------------

def get_category_by_id(category_id: int, db: Session, *, attrs: list[str] = None):
    return get_one(db, Category, category_id, attrs=attrs)


def get_all_categories(db: Session, *, attrs: list[str] = None):
    return get_all(db, Category, attrs=attrs)


# ------------------------------ UPDATE --------------------------------

# ------------------------------ DELETE --------------------------------
