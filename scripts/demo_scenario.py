"""
Trigger the prepared scenario from the command line as a presentation backup.
"""
import json, urllib.request

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/ai/predict-and-reschedule",
    data=json.dumps({"date": "2026-05-19", "city": "Ankara"}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
print(json.dumps(json.loads(urllib.request.urlopen(req).read()), indent=2, ensure_ascii=False))
