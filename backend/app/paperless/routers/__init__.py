from .category import router as category_router
from .utility import router as utility_router
from .year import router as year_router
from .document_type import router as document_type_router
from .document import router as document_router
from .path import router as path_router
from .form import router as form_router

__all__ = [
    'category_router',
    'utility_router',
    'year_router',
    'document_type_router',
    'document_router',
    'path_router',
    'form_router'
]