import os
import sys

# Add backend/ to the import path regardless of the working directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import personnel, leave_requests, schedule, ai

app = FastAPI(
    title="YAP-İS | Yapay Zeka Destekli İzin Planlayıcısı",
    description="Predictive Healthcare Management — hava + AI + iş mantığı entegrasyonu",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(personnel.router,      prefix="/api/personnel",      tags=["Personnel"])
app.include_router(leave_requests.router, prefix="/api/leave-requests", tags=["Leave Requests"])
app.include_router(schedule.router,       prefix="/api/schedule",       tags=["Schedule"])
app.include_router(ai.router,             prefix="/api/ai",             tags=["AI Predictive"])


@app.get("/api")
def api_root():
    return {"message": "YAP-İS API hazır. /docs adresine gidin."}


# Serve the frontend from the same origin for the single-process demo.
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
