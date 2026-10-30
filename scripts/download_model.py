"""
Download the CatBoost model and CSV files from Drive into data/.
Requires accessible Drive shares; overwrites existing files.
"""
import os, urllib.request

FILES = {
    "catboost_er_model.cbm": "1tImmnu7c4lf6I2Iu3PJHMQPY5JNyGEw3",
    "er_dataset_ankara.csv": "1NSZlCS6whHlR1xmAmBEbDVStEY3uYMqS",
    "forecast_next_days.csv": "1lweww6O_RHuROit49g_p6Mdy7kz8a_An",
    "feature_importance.csv": "1Q7KlA0LqDOnqEDIkeYizC_cS5xo3FbNi",
}
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

for name, fid in FILES.items():
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    dst = os.path.join(OUT, name)
    print(f"⬇️  {name}")
    urllib.request.urlretrieve(url, dst)
print("✅ Done.")
