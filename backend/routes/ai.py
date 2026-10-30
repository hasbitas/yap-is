"""
AI prediction and leave-rescheduling routes.

Obtain simulated weather and call the in-process predictor. Compare demand
with the baseline and move approved leave to next Thursday if at least 20%
higher. Return leave updates and a seven-day forecast in one response.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.mock_data import leave_requests_db, schedule_db
from services.weather import get_weather_forecast
from services.ai_predictor import predict as ai_predict_local

router = APIRouter()

BASELINE_PATIENTS = 330.0   # Demo reference patient count.
SURGE_THRESHOLD = 0.20      # An increase of at least 20% triggers rescheduling.


class PredictRequest(BaseModel):
    date: str           # "2026-05-19"
    city: str = "Ankara"


def _shift_leaves_to(target_date: str, source_date: str) -> List[Dict[str, Any]]:
    """Move approved leave records from the source date to the target date."""
    moved = []
    for req in leave_requests_db:
        if req["start_date"] == source_date and req["status"] == "approved":
            req["original_date"] = source_date
            req["start_date"] = target_date
            req["end_date"] = target_date
            req["status"] = "rescheduled"
            req["reschedule_reason"] = "AI: Hava durumu kaynaklı vaka artışı öngörüsü"
            moved.append(req)
    return moved


DAYS_TR = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
DAYS_TR_SHORT = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
CAPACITY = 1000.0


def _classify(ratio: float) -> tuple[str, str]:
    """Convert a capacity ratio to a demand label and color."""
    if ratio >= 0.85:
        return "Çok Yüksek", "red"
    if ratio >= 0.65:
        return "Yüksek", "red"
    if ratio >= 0.50:
        return "Orta", "yellow"
    if ratio >= 0.35:
        return "Düşük", "green"
    return "Çok Düşük", "green"


@router.post("/predict-and-reschedule")
def predict_and_reschedule(payload: PredictRequest):
    """Run weather, prediction, leave rules, and the seven-day forecast."""
    weather = get_weather_forecast(payload.city, payload.date)
    ai_result = ai_predict_local(payload.date, weather)

    weekly_forecast = []
    start = datetime.strptime(payload.date, "%Y-%m-%d")
    for i in range(7):
        d = start + timedelta(days=i)
        ds = d.strftime("%Y-%m-%d")
        w = get_weather_forecast(payload.city, ds)
        pr = ai_result if i == 0 else ai_predict_local(ds, w)
        pred = float(pr["predicted_er_patients"])
        ratio = pred / CAPACITY
        intensity, status = _classify(ratio)
        weekly_forecast.append({
            "date": ds,
            "date_tr": d.strftime("%d.%m.%Y"),
            "weekday": DAYS_TR[d.weekday()],
            "weekday_short": DAYS_TR_SHORT[d.weekday()],
            "predicted": round(pred),
            "ratio": round(ratio, 3),
            "intensity": intensity,
            "status": status,
            "tavg": w.get("tavg"),
            "condition": w.get("condition"),
            "is_selected": i == 0,
        })

    predicted = float(ai_result["predicted_er_patients"])
    surge_pct = round((predicted - BASELINE_PATIENTS) / BASELINE_PATIENTS * 100, 1)

    # 3) Move leave records when the surge threshold is reached.
    moved_leaves: List[Dict[str, Any]] = []
    action_taken = "no_action"
    target_date = None
    if surge_pct >= SURGE_THRESHOLD * 100:
        src = datetime.strptime(payload.date, "%Y-%m-%d")
        # Move to next Thursday (weekday index 3).
        delta = (3 - src.weekday()) % 7 or 7
        target_date = (src + timedelta(days=delta)).strftime("%Y-%m-%d")
        moved_leaves = _shift_leaves_to(target_date, payload.date)
        action_taken = "leaves_rescheduled" if moved_leaves else "no_leaves_to_move"

    # 4) Return one response for the frontend.
    return {
        "status": "success",
        "scenario_date": payload.date,
        "weather": weather,
        "ai_prediction": {
            "predicted_er_patients": round(predicted),
            "baseline": int(BASELINE_PATIENTS),
            "surge_pct": surge_pct,
            "top_risks": ai_result.get("top_risks", []),
            "model": ai_result.get("model", "catboost"),
        },
        "operational_response": {
            "action": action_taken,
            "rescheduled_to": target_date,
            "moved_leaves": moved_leaves,
            "message": (
                f"⚠️ {payload.date} için %{surge_pct} vaka artışı öngörüldü. "
                f"{len(moved_leaves)} doktor izni otomatik olarak {target_date} tarihine kaydırıldı."
                if moved_leaves else
                f"Tahmin {payload.date} için normal aralıkta (%{surge_pct}). Müdahale gerekmedi."
            ),
        },
        "updated_schedule": schedule_db,
        "updated_leaves": leave_requests_db,
        "weekly_forecast": weekly_forecast,
    }


@router.post("/optimize-schedule")
def optimize_schedule():
    """Mock optimizer retained for backward compatibility."""
    return {
        "status": "success",
        "message": "Mock optimizasyon tamamlandı.",
        "data": schedule_db,
    }
