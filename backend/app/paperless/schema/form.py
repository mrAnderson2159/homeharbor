# backend/app/paperless/schema/form.py

from typing import Optional, Literal
from pydantic import BaseModel

class FieldMeta(BaseModel):
    id: str
    label: str
    type: Literal["text", "number", "select", "date"]
    placeholder: Optional[str] = None
    required: bool = True
    min: Optional[int] = None
    max: Optional[int] = None
    options: Optional[list[str] | list[dict[str, str]]] = None  # per i select
    autocomplete: Optional[list[str]] = None
