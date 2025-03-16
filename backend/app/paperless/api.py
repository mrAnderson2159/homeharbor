# backend/app/paperless/api.py

from fastapi import APIRouter
from app.paperless.routers import *

paperless_router = APIRouter(prefix="/paperless", tags=["Paperless"])

paperless_router.include_router(category_router)
paperless_router.include_router(utility_router)
paperless_router.include_router(document_router)
paperless_router.include_router(form_router)
