from fastapi import APIRouter, HTTPException
from services.mock_data import leave_requests_db

router = APIRouter()


@router.get("/")
def get_pending_leave_requests():
    """Return leave requests awaiting approval."""
    pending = [r for r in leave_requests_db if r["status"] == "pending"]
    return {"status": "success", "data": pending}


@router.get("/all")
def get_all_leave_requests():
    return {"status": "success", "data": leave_requests_db}


@router.post("/{request_id}/approve")
def approve_leave_request(request_id: int):
    for req in leave_requests_db:
        if req["id"] == request_id:
            req["status"] = "approved"
            return {"status": "success", "data": req}
    raise HTTPException(status_code=404, detail="İzin talebi bulunamadı.")


@router.post("/{request_id}/reject")
def reject_leave_request(request_id: int):
    for req in leave_requests_db:
        if req["id"] == request_id:
            req["status"] = "rejected"
            return {"status": "success", "data": req}
    raise HTTPException(status_code=404, detail="İzin talebi bulunamadı.")
