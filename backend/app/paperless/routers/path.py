from fastapi import APIRouter
from app.paperless.schema.response import PathSchema

router = APIRouter(prefix="/paths", tags=["Paths"])