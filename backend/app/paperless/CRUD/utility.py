from sqlalchemy.orm import Session

from app.paperless.models import Utility
from app.paperless.routers.functions import get_one, get_all

# ------------------------------ CREATE --------------------------------

# ------------------------------ READ --------------------------------

def get_utility_by_id(utility_id: int, db: Session, *, attrs: list[str] = None):
    return get_one(db, Utility, utility_id, attrs=attrs)


def get_all_utilities(db: Session, *, attrs: list[str] = None):
    return get_all(db, Utility, attrs=attrs)


# ------------------------------ UPDATE --------------------------------

# ------------------------------ DELETE --------------------------------
