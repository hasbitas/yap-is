"""
In-process ER patient-count prediction; no separate HTTP port.

Use a compatible CatBoost model if available, otherwise a repeatable weather
formula. The default demo needs only FastAPI, Uvicorn, and Pydantic.
"""
from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
MODEL_PATH = os.path.join(DATA_DIR, "catboost_er_model.cbm")

_model = None
_tried = False


def _try_load():
    global _model, _tried
    if _tried:
        return
    _tried = True
    if not os.path.exists(MODEL_PATH):
        return
    try:
        from catboost import CatBoostRegressor  # type: ignore
        m = CatBoostRegressor()
        m.load_model(MODEL_PATH)
        _model = m
    except Exception:
        _model = None


def _heuristic(date: str, w: Dict) -> float:
    d = datetime.strptime(date, "%Y-%m-%d")
    base = 330.0
    tavg = float(w.get("tavg", 15.0))
    temp_effect = max(0.0, (15.0 - tavg)) * 8.5
    snow_effect = float(w.get("snow", 0.0)) * 6.0
    prcp_effect = float(w.get("prcp", 0.0)) * 3.0
    dow_mult = {0: 1.05, 1: 1.10, 2: 1.02, 3: 0.95, 4: 0.92, 5: 0.70, 6: 0.65}[d.weekday()]
    return round((base + temp_effect + snow_effect + prcp_effect) * dow_mult, 1)


def _top_risks(w: Dict) -> List[str]:
    risks = []
    if w.get("tavg", 20) <= 0:
        risks.append("Donma kaynaklı düşme / kırık vakalarında artış")
    if w.get("snow", 0) > 0:
        risks.append("Trafik kazaları ve hipotermi riski")
    if w.get("tavg", 20) <= 5:
        risks.append("Üst solunum yolu enfeksiyonu / grip salgını ivmesi")
    if not risks:
        risks.append("Normal mevsim profili")
    return risks


def predict(date: str, weather: Dict) -> Dict:
    _try_load()
    w = weather or {}
    model_name = "heuristic_fallback"
    pred = _heuristic(date, w)

    if _model is not None:
        try:
            import numpy as np
            d = datetime.strptime(date, "%Y-%m-%d")
            x = np.array([[
                w.get("tavg", 15), w.get("tmin", 10), w.get("tmax", 20),
                w.get("prcp", 0), w.get("snow", 0), w.get("snow_day", 0),
                d.weekday(), d.year, int(d.weekday() >= 5),
            ]])
            pred = float(_model.predict(x)[0])
            model_name = "catboost_er_model"
        except Exception:
            pass  # Keep the heuristic result.

    return {
        "predicted_er_patients": round(pred, 1),
        "model": model_name,
        "top_risks": _top_risks(w),
        "input_date": date,
        "weather_used": w,
    }
