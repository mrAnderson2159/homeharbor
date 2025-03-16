from fastapi import APIRouter
from app.paperless.api import paperless_router

api_router = APIRouter(prefix="/api", tags=["Api"])
api_router.include_router(paperless_router)