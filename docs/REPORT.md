# Project Report — YAP-IS: AI Leave Planner

## Why was it built?

The project explores a staffing problem: unexpected emergency-room demand can leave too few staff available, increase waiting times, and add pressure on doctors. Its original motivation cited sudden winter increases of **30–80%** in emergency-room visits in Türkiye, linked to flu, falls on ice, and hypothermia. This figure is retained from the original report; no supporting study is included in this repository, so it is not an independently verified health statistic.

The original goal was to predict demand **48 hours ahead** using weather, weekdays, public holidays, and historical trends, then move leave away from risky days. The current demo instead accepts a selected date, generates simulated weather, and calculates a seven-day forecast. It does not implement a separate 48-hour alert system. The browser offers a **two-leave weekly allowance**, reset when the ISO week changes; this is a demo interaction, not a server-enforced hospital policy.

## How does the system work?

1. A doctor signs in with a fake account and sees sample weekly leave recommendations.
2. The user selects a date and presses **Yapay Zeka Analizini Başlat** (Start AI analysis).
3. The backend generates weather for that date, using prepared scenarios or a repeatable seasonal profile for Ankara. It does not contact a weather provider.
4. The backend's built-in predictor estimates the number of ER (emergency-room) patients. It uses a compatible CatBoost model if available, otherwise a heuristic fallback: a fixed formula using temperature, snow, rain, and weekday.
5. It compares the estimate with a **330-patient baseline**. If the increase is **at least 20%**, approved leave records starting on the selected date move to the **next Thursday**. That destination is fixed; the code does not search for an optimal day.
6. It calculates **seven daily forecasts**, with five demand labels: Very Low, Low, Medium, High, and Very High. Labels compare predictions with a demo capacity of **1,000 patients**.
7. The frontend draws a seven-day bar chart, outlines the selected date, rebuilds the leave recommendations, and shows a weather-related operational notice. The chart colors reflect demand levels. Weekly browser leave selections reset when the ISO week changes.

The duty schedule itself stays as sample data; the rescheduling operation changes leave records in server memory.

## Technology used

| Layer | Technology | Role |
| --- | --- | --- |
| Frontend | HTML5, CSS3, JavaScript (ES6) | Dashboard, demo sign-in, summary cards, chart, leave table, dark mode. |
| Backend | Python 3.9+, FastAPI, Uvicorn, Pydantic | API, leave rules, simulated weather, built-in predictor, static frontend hosting on port 8000. The original report listed Python 3.11; this documentation run used 3.12. |
| Optional AI service | Python, FastAPI, CatBoost, NumPy, Pandas | Separate predictor on port 9000, with fallback if the model is unavailable. Not used by the standard backend. |
| Communication | Browser fetch requests | Browser to backend. The original report described asynchronous `httpx` calls to the AI service; the current backend calls its predictor directly and does not require `httpx`. |
| Data | Optional CatBoost `.cbm` model and Ankara ER CSV files | Large files are downloaded separately. The tracked feature-importance table includes `tavg`, `dayofweek`, `prcp`, `snow`, and `holiday_type`; this does not mean all of them feed the fallback formula. |
| Launchers | `scripts/run_all.bat` and `scripts/run_all.sh` | Install the three core packages and start one backend process that also serves the frontend. |

## Repository structure

```text
backend/    Server on 8000: staff, leave, schedule, and AI routes; local services
frontend/   Turkish dashboard, served by the backend
ai/         Optional standalone CatBoost/fallback server on 9000
data/       Feature importance and optional downloaded model/datasets
scripts/    Launchers, download_model.py, and demo_scenario.py
docs/       This project report
```

See the [main README](../README.md) for setup and the [data guide](../data/README.md) for file availability.

## Prepared demo scenario

**19 May 2026 (Tuesday), -5°C, snow:**

- Prediction: **598 patients**, against a baseline of **330**, approximately **81% higher**. These rounded figures are reproducible with the fallback formula; they are not evidence of model accuracy.
- Displayed risks: falls on ice, traffic accidents, hypothermia, and respiratory illness. These are scripted weather-based messages, not clinical diagnoses.
- Action: **three approved staff leave records** move from Tuesday to **Thursday, 21 May 2026**. The original report called these three doctors; the actual sample records are two doctors and one nurse.
- Frontend: a warning banner, updated leave recommendations, and the selected Tuesday outlined on the chart. With 598/1,000 patients, the chart classifies that day as **Medium**, even though it exceeds the leave-moving threshold.

Restart the backend to restore the three original leave records before repeating the scenario. No real hospital data is changed.

## Outcome and evidence limits

The demo connects date selection, simulated weather, prediction, leave rescheduling, and dashboard updates in one interaction. Dates outside the prepared scenarios use a **synthetic seasonal profile** rather than a live weather dataset.

The original report stated that this flow completed in **under 300 ms** during the presentation. That historical claim is preserved here, but this repository contains no benchmark supporting it; it is not a measured guarantee for a new machine or browser.

This is a portfolio prototype, **not a medical product**. Neither the optional trained model's accuracy nor the fixed leave-moving policy has been validated here for hospital use. See [Limitations](../README.md#limitations).
