from fastapi import APIRouter
from services.mock_data import personnel_db

router = APIRouter()


@router.get("/")
def get_personnel():
    """List staff and their availability or duty status."""
    return {"status": "success", "data": personnel_db}
