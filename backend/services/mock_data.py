# In-memory database simulation.
# Sample records for the hackathon demo.

personnel_db = [
    {"id": 1, "name": "Dr. Ayşe Yılmaz", "specialty": "Kardiyoloji", "total_hours": 42, "status": "available"},
    {"id": 2, "name": "Dr. Mehmet Demir", "specialty": "Nöroloji", "total_hours": 36, "status": "on_leave"},
    {"id": 3, "name": "Hemşire Elif Kaya", "specialty": "Acil Servis", "total_hours": 48, "status": "on_duty"},
    {"id": 4, "name": "Dr. Canan Şahin", "specialty": "Dahiliye", "total_hours": 40, "status": "available"},
    {"id": 5, "name": "Hemşire Burak Çelik", "specialty": "Yoğun Bakım", "total_hours": 50, "status": "available"},
]

leave_requests_db = [
    {"id": 101, "personnel_id": 2, "personnel_name": "Dr. Mehmet Demir",
     "start_date": "2026-05-19", "end_date": "2026-05-19",
     "reason": "Yıllık İzin", "status": "approved"},
    {"id": 102, "personnel_id": 5, "personnel_name": "Hemşire Burak Çelik",
     "start_date": "2026-05-19", "end_date": "2026-05-19",
     "reason": "Hastalık İzni", "status": "approved"},
    {"id": 103, "personnel_id": 4, "personnel_name": "Dr. Canan Şahin",
     "start_date": "2026-05-19", "end_date": "2026-05-19",
     "reason": "İdari İzin", "status": "approved"},
]

# Prepared dates: Tuesday 2026-05-19 and Thursday 2026-05-21.
schedule_db = [
    {"id": 1001, "personnel_id": 1, "personnel_name": "Dr. Ayşe Yılmaz",
     "date": "2026-05-19", "shift": "08:00 - 16:00", "department": "Kardiyoloji Polikliniği"},
    {"id": 1002, "personnel_id": 3, "personnel_name": "Hemşire Elif Kaya",
     "date": "2026-05-19", "shift": "16:00 - 00:00", "department": "Acil Servis"},
    {"id": 1003, "personnel_id": 4, "personnel_name": "Dr. Canan Şahin",
     "date": "2026-05-21", "shift": "08:00 - 16:00", "department": "Dahiliye Polikliniği"},
]
