# YAP-İS — Yapay Zeka Destekli İzin Planlayıcısı

> **Predictive Healthcare Management** — Hava durumu + hafta günü + hastalık trendlerini birleştiren AI, acil servis yoğunluğunu öngörüp doktor izinlerini otonom planlar.

## 🚀 Tek Komutla Çalıştırma

**Windows:**
```cmd
git clone https://github.com/hasbitas/yapay_zeka_destekli_izin_zamanlay-c-_sistemi.git
cd yapay_zeka_destekli_izin_zamanlay-c-_sistemi
scripts\run_all.bat
```

**Linux / macOS:**
```bash
git clone https://github.com/hasbitas/yapay_zeka_destekli_izin_zamanlay-c-_sistemi.git
cd yapay_zeka_destekli_izin_zamanlay-c-_sistemi
bash scripts/run_all.sh
```

→ Tarayıcı otomatik açılır: `http://127.0.0.1:8000/` • Login: `AY001 / ayse123`

## 🔧 Gereksinimler (minimum)

- Python 3.9+ (Windows: kurarken **"Add Python to PATH"** işaretle)
- İnternet (sadece ilk açılışta `pip install` için)

> Sadece `fastapi`, `uvicorn`, `pydantic` kurulur. CatBoost **opsiyonel**: model dosyası `data/catboost_er_model.cbm` varsa kullanılır, yoksa deterministik heuristic fallback devreye girer ve demo aynı şekilde çalışır.

## 📁 Repo

```
backend/   FastAPI (port 8000) — frontend'i de servis eder, AI tahmini in-process
frontend/  YAP-İS dashboard (vanilla HTML/CSS/JS)
ai/        Opsiyonel ayrı mikroservis (tek port modunda gerekmez)
data/      Model + dataset
scripts/   run_all.bat (Windows) • run_all.sh (Linux/Mac)
```

## 🎬 Senaryo

Dashboard'da tarih seç → **🤖 Yapay Zeka Analizini Başlat** → 7 günlük forecast, kaydırılan izinler, hava durumu uyarısı.

Detaylı sistem mimarisi ve teknoloji yığını için: [RAPOR.md](./RAPOR.md)
