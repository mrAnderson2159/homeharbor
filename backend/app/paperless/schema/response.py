# backend/app/paperless/schema/response.py
from typing import Optional

from app.paperless.schema.base import BaseSchema, DescriptionSchema, OrmSchema


class CategorySchema(DescriptionSchema, OrmSchema):
    pass


class UtilitySchema(DescriptionSchema, OrmSchema):
    pass


class YearSchema(BaseSchema, OrmSchema):
    pass


class DocumentTypeSchema(DescriptionSchema, OrmSchema):
    pass


class DocumentSchema(DescriptionSchema, OrmSchema):
    tags: Optional[list[str]] = None


class PathSchema(OrmSchema):
    id: int
    category: str
    utility: str
    year: str
    document_type: str
    document: str


class PendingScanSchema(OrmSchema):
    id: int
    category: str
    utility: str
    year: str
    document_type: str
    document: str

