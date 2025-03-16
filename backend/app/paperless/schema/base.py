# backend/app/paperless/schema/base.py
from typing import Optional
from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int
    name: str


class DescriptionSchema(BaseSchema):
    description: Optional[str] = None


class OrmSchema(BaseModel):
    class Config:
        from_attributes = True
        extra = "forbid"  # vieta campi sconosciuti nei model


class BaseCreationSchema(BaseModel):
    name: str


class DescriptionCreationSchema(BaseCreationSchema):
    description: Optional[str] = None
