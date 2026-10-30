# Data files

The standard demo works without downloading a model or dataset. Only
`feature_importance.csv` is tracked here. Large model and dataset files are ignored by Git.

| File | Purpose | Included in Git? |
| --- | --- | --- |
| `catboost_er_model.cbm` | Optional trained CatBoost patient-count model. | No |
| `er_dataset_ankara.csv` | Ankara emergency-room training dataset, as described by the original project. | No |
| `forecast_next_days.csv` | Original 14-day forecast export; not the dashboard's live seven-day response. | No |
| `feature_importance.csv` | Small table ranking model inputs; a reference for the project's prediction design. | Yes |

To fetch all four files, run `python scripts/download_model.py` from the repository root.
This uses four Google Drive file IDs embedded in that script. The shares must be
accessible, and downloads may fail if sharing permissions change. The script can
overwrite existing files, including `feature_importance.csv`. The downloads and
training data were not independently verified in this documentation pass.

Installing the core requirements does not install CatBoost. Optional model setup
is explained in the [README](../README.md#optional-model-and-separate-ai-server).
Without a usable model, the backend uses a repeatable heuristic formula. Weather
is generated in code, not read from these CSV files. No live hospital or weather
feed is connected.
