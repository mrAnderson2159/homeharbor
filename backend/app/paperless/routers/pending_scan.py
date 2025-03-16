from fastapi import APIRouter
from app.paperless.schema.response import PendingScanSchema

router = APIRouter(prefix="/pending_scans", tags=["Pending Scans"])