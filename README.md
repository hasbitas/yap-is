# YAP-IS — AI Leave Planner for Hospital Doctors

A local demo that estimates emergency-room demand from simulated weather and moves staff leave when a busy day is expected.

## What does it do?

Choose a date to see how weather could affect a hospital's staffing needs.
The app estimates patient numbers for that date and the following six days.
For example: a snowy-day forecast -> higher expected demand -> approved doctor leave moved to the next Thursday.
You can see the predicted demand, weather warning, and leave recommendations on one dashboard.
The user interface is in Turkish because the project targets Turkish hospitals.

## Demo preview

<!-- DEMO_VIDEO -->

Demo video slot: add a recording here. No video is included yet.

## Quick start (5 minutes)

Allow extra time for the first package download. You do not need coding experience, Node.js, a graphics card, or the optional model download.

1. Install **Python 3.9+** from [python.org](https://www.python.org/downloads/).
   On Windows, tick **Add Python to PATH**, then reopen your terminal.
   The local run for this documentation used Python 3.12.
2. [Open the repository](https://github.com/hasbitas/yap-is), click **Code -> Download ZIP**, and extract it.
   Or, if you already have Git, open a terminal and run:
   ```text
   git clone https://github.com/hasbitas/yap-is.git
   cd yap-is
   ```
3. Open a terminal in the extracted or cloned project folder and start the demo.
   **Windows** (Command Prompt or PowerShell):
   ```text
   scripts\run_all.bat
   ```
   **macOS/Linux**:
   ```sh
   bash scripts/run_all.sh
   ```
   The script installs the required packages using your selected Python and starts the server.
   It does not create a virtual environment; developers can use the isolated setup below.
4. On Windows, your browser opens **http://127.0.0.1:8000/** automatically.
   On macOS/Linux, open that address yourself. If the first page load fails, wait for the server to finish starting and refresh.
5. Sign in with **AY001 / ayse123** (Doctor ID / password), then press **Giriş Yap** (Sign in).
   This is a **fake demo account**, stored in the browser code, not a real hospital login.
6. Keep the terminal open while using the app. To stop it, press **Ctrl+C** in that terminal.

## Try the demo

1. Pick **19 May 2026** (`2026-05-19`) in the date field.
2. Press **🤖 Yapay Zeka Analizini Başlat** (**Start AI analysis**).
3. Look for the weather warning, updated seven-day chart, and leave recommendations.
   Without the optional model, this scenario predicts **598 patients**, compared with a reference of **330** (about **81% more**).
   Three approved staff leave records (two doctors and one nurse) move to **21 May 2026**, the next Thursday.
4. Try another date to compare results. Restart the server to restore the original sample leave records;
   repeating the same analysis after the move will not move those records again.

## How it works

The **frontend** is the page you see in the browser. It sends a date to the **backend**,
the Python program that handles requests. The backend makes simulated weather and a
**forecast**, an estimate of future patient numbers. It uses **CatBoost**, a machine-learning
prediction tool, if a compatible model and its packages are available. Otherwise it uses a
**heuristic fallback**, a repeatable formula based on temperature, snow, rain, and day of week.

```text
Selected date -> simulated weather -> patient estimate
                                    -> compare with 330 patients
                                    -> if at least 20% higher, move approved leave to next Thursday
                                    -> return seven-day chart + leave updates to browser
```

**ER** means emergency room. The chart compares daily estimates with a demo capacity of
1,000 patients; the leave-moving rule instead compares them with the 330-patient reference.
Thursday is a fixed rule, not a search for the safest available day.

## Folder guide

| Folder / file | What you will find |
| --- | --- |
| `frontend/` | Turkish dashboard and fake demo sign-in, built with HTML, CSS, and JavaScript. |
| `backend/` | Web server, staff and leave routes, simulated weather, and built-in prediction logic. |
| `ai/` | Optional standalone prediction server; not needed by the default demo. |
| `data/` | Small feature-importance table; optional large files are described in [the data guide](data/README.md). |
| `scripts/` | Launchers, optional file downloader, and command-line demo request. |
| `requirements.txt` | The three direct dependencies needed for the standard demo. |
| `docs/REPORT.md` | [Project report](docs/REPORT.md), including original demo figures and their limits. |

## Troubleshooting

| Problem | What to try |
| --- | --- |
| Python is not found | Install Python 3.9+, enable **Add Python to PATH** on Windows, and reopen the terminal. On macOS/Linux, check `python3 --version`. |
| pip installation fails | Check the first error and your internet connection. Use the isolated setup below if your system Python blocks package installation. On Linux, you may need your distribution's `python3-venv` package. |
| Port 8000 is busy | Stop an earlier demo terminal with Ctrl+C, or close the application using that port, then retry. Do not stop an unfamiliar process. |
| CatBoost model is missing | This is normal: the heuristic fallback keeps the demo working. No model download or CatBoost installation is required. |
| Browser does not open or cannot connect | On macOS/Linux, open http://127.0.0.1:8000/ manually. On any system, keep the server terminal open, wait for startup, and refresh. |
| The leave records do not move again | The demo keeps changes in memory. Restart the server and use `2026-05-19` to restore and repeat the prepared scenario. |

## For developers

The standard server serves both the page and the **API** (the routes other programs use to exchange data) on **8000**.
There is no separate frontend server. Run commands from the repository root.

### Isolated manual setup

Windows / PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe backend/main.py
```

macOS/Linux:

```sh
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python backend/main.py
```

No environment activation is needed for these commands. `.venv/` is ignored by Git.
Stop the server with Ctrl+C. The server binds to `0.0.0.0`, so it may also be reachable
from other machines on your network; use it as a local demo.

### API routes

Open http://127.0.0.1:8000/docs for interactive request documentation.

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api` | Basic server message. |
| GET | `/api/personnel/` | List sample staff. |
| GET | `/api/leave-requests/` | List pending leave requests. |
| GET | `/api/leave-requests/all` | List all leave requests. |
| POST | `/api/leave-requests/{request_id}/approve` | Approve a request. |
| POST | `/api/leave-requests/{request_id}/reject` | Reject a request. |
| GET | `/api/schedule/` | List the sample duty schedule. |
| POST | `/api/ai/predict-and-reschedule` | Analyze `{"date":"2026-05-19","city":"Ankara"}` and update matching leave records. |
| POST | `/api/ai/optimize-schedule` | Legacy mock response; returns the sample schedule. |

With the backend running, send the prepared scenario from a second terminal:

```text
python -X utf8 scripts/demo_scenario.py
```

Use your `.venv` Python path instead of `python` if you used the isolated setup.
The `-X utf8` option lets Windows print the Turkish text and emoji reliably.
The script prints the response and changes only the running server's in-memory leave records.

### Optional model and separate AI server

`python scripts/download_model.py` downloads the model and supporting CSV files from Google Drive into `data/`.
It needs internet and accessible Drive shares; it can overwrite existing files, including the tracked feature-importance CSV.
The four Drive file IDs are download sources, not API credentials. The default demo does not need them.

For optional CatBoost support, install `ai/requirements.txt` using your chosen Python:
`python -m pip install -r ai/requirements.txt`. Place the compatible model at
`data/catboost_er_model.cbm`. The backend tries to load it and falls back if loading or prediction fails.

To start the optional standalone service, run `python ai/predictor.py` in another terminal.
It listens on **9000**, with `GET /` for model status and `POST /predict` accepting
`{"date":"2026-05-19","weather":{"tavg":-5,"snow":6,"prcp":2.4}}`.
The standard backend **does not call this service**; it uses its own prediction code.
No model quality or compatibility is established by the fallback demo.

## Glossary

The terms frontend, backend, forecast, CatBoost, heuristic fallback, ER, and API are explained where they first appear above.

| Term | Meaning |
| --- | --- |
| Baseline | The reference patient count used for comparison: 330 in this demo. |
| Mock / synthetic data | Invented examples or generated values rather than live hospital records. |
| Model | A saved prediction program fitted to data. |
| Feature | An input to a prediction, such as temperature or day of week. |
| Port | A numbered connection point on your computer, such as 8000. |
| Virtual environment | A project-specific Python package folder, here `.venv`. |

## Limitations

This is a portfolio prototype using **mock staff records and synthetic weather**, not a medical product.
Weather is mocked, not fetched from a live provider. The default prediction is a formula, not a validated clinical forecast.
There is no persistent database: server changes disappear on restart, and browser leave selections are demo state.
The frontend's two-leave weekly allowance is not enforced as a backend policy.
The demo login is visible in JavaScript and the API has no authentication; do not use real patient or staff information.
The fixed Thursday rule does not check staffing constraints or prove that a day is safe for leave.

## License

MIT. See [LICENSE](LICENSE).
