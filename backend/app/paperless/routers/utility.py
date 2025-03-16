# backend/app/paperless/routers/utility.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.paperless.CRUD.utility import get_utility_by_id, get_all_utilities
from app.paperless.schema.response import UtilitySchema

router = APIRouter(prefix="/utilities", tags=["Utilities"])


@router.get("/{utility_id}", response_model=UtilitySchema)
def _get_utility_by_id(utility_id: int, db: Session = Depends(get_db)):
    return get_utility_by_id(utility_id, db)


@router.get("/", response_model=list[UtilitySchema])
def _get_utilities(db: Session = Depends(get_db)):
    return get_all_utilities(db)
