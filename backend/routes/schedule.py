from fastapi import APIRouter
from services.mock_data import schedule_db

router = APIRouter()


@router.get("/")
def get_schedule():
    """Return the sample duty schedule."""
    return {"status": "success", "data": schedule_db}
