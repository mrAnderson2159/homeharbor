from fastapi import APIRouter
from app.paperless.schema.response import YearSchema

router = APIRouter(prefix="/years", tags=["Years"])