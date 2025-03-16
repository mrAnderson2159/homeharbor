# backend/app/paperless/schema/creation.py
from typing import Optional
from pydantic import BaseModel

from app.paperless.schema.base import BaseCreationSchema, DescriptionCreationSchema


class CategoryCreationSchema(DescriptionCreationSchema):
    pass


class UtilityCreationSchema(DescriptionCreationSchema):
    pass


class YearCreationSchema(BaseCreationSchema):
    pass


class DocumentTypeCreationSchema(DescriptionCreationSchema):
    pass


class DocumentCreationSchema(DescriptionCreationSchema):
    pages: Optional[int] = None


class PathCreationSchema(BaseModel):
    category_id: int
    utility_id: int
    year_id: int
    document_type_id: int
    document_id: int


class TagCreationSchema(BaseCreationSchema):
    pass


class DocumentTagCreationSchema(BaseModel):
    document_id: int
    tag_id: int


class ExcludedPathCreationSchema(BaseModel):
    path: str
    reason: Optional[str] = None
