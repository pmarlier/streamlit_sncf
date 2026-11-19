# 🚄 Streamlit SNCF — TGV punctuality explorer
 
Interactive app to explore the punctuality of the TGV network
and understand what causes delays, route by route, month by month, year by year.
 
It is built on the SNCF open dataset
[*Régularité mensuelle TGV*](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/information/)
and developed as the IADATA700 project by Pierre Marlier,
Ulysse Perruchon-Monge and Christophe Vandenborre.
 
🔗 **Live app:** _to be added once deployed (Streamlit Community Cloud)_
 
---
 
## What the app does
 
The question driving the app: **"How reliable is my train, and why is it sometimes late?"**
 
Two entry points on the home page:
 
| Mode | What you get |
| --- | --- |
| **National statistics** | A map of the TGV network where each line is coloured by its mean arrival delay (slider to filter a delay range), and a pie chart of the delay causes averaged over the whole period. |
| **A specific trip** | Pick a departure station, an arrival station, a period (months + years) in the sidebar to get the monthly arrival-delay graph, the breakdown of delay causes for that route, the route drawn on the map, and a table of delayed / cancelled train ratios. |
 
Delay causes shown: SNCF causes, passengers causes and others.
 
## Project structure
 
```text
.
├── src/
│   ├── streamlit_sncf_app.py      # Entry point of the Streamlit app
│   ├── core/                      # Back-end modules and functions
│   │   ├── load_data.py           #   CSV loading + query helpers on the dataframe
│   │   ├── data_preprocessing.py  #   Cleaning pipeline (see "Data" below)
│   │   ├── railway_data/          #   Station names / railway geometry matching
│   │   └── statistics/            #   Mean delay, delay causes, train counts, seasonality
│   └── ui/                        # Front-end modules and functions
│       ├── carto/                 #   Folium map and railway drawing
│       └── widgets/               #   Sidebar, graphs, pie chart, stats table
├── tests/                         # pytest functions, testing src/
├── data/
│   ├── raw/                       # Source CSV files (see "Data")
│   ├── processed/                 # Generated files (git-ignored)
│   └── DATASHEET_FOR_DATASET.md   # Documentation of the datasets
├── config/logging.conf            # Logging configuration
├── docs/                          # Sphinx documentation (AutoAPI)
│   ├── _other/                    # Other ressources
│   │   ├── sphinx_utilisation.md  #   Sphinx utilisation guidelines
│   │   └── dataseet_for_dataset.md#   Datasheet for dataset
│   └── sphinx_conf_files          # Sphinx configuration files
├── resources/                     # Logos and icons used by the UI
├── .github/workflows/             # CI (tests) and Docker build
├── Dockerfile
└── pyproject.toml                 # Dependencies and tool configuration (uv)
```
 
The code is split in two layers: `core` computes, `ui` displays. `core` never imports
anything from `ui`.
 
## Getting started
 
### Prerequisites
 
- Python **3.12** or later (see `.python-version`)
- [`uv`](https://docs.astral.sh/uv/) (`pip install uv`)

### Install

```bash
git clone https://github.com/pmarlier/streamlit_sncf.git
cd streamlit_sncf
uv sync --dev
```

 This app requires the following dependencies:
 - Python (>=3.12)
 - pandas
- pydeck
- streamlit
- seaborn
- matplotlib-inline
- ipykernel
- sphinx
- sphinx-autoapi
- streamlit-folium
- unidecode
- geopy
- plotly
- colorlog
- colorama
- mypy
- pre-commit
- pytest
- pytest-cov
- ruff


 
### Data
 
The following CSV file is expected in `data/raw/`:
 
| File | Used for |
| --- | --- |
| `regularite-mensuelle-tgv-aqst.csv` | Monthly regularity per TGV route (main dataset) |
 
To refresh the main file, download the latest export from
[data.sncf.com](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/export/)
and replace it in `data/raw/` (keep the same file name). More details in
[`docs/_other/datasheet_for_dataset.md`](docs/_other/datasheet_for_dataset.md).
 
### Run the app
 
Always run from the **repository root**, because file paths (`data/`, `config/`,
`resources/`) are relative:
 
```bash
uv run streamlit run src/streamlit_sncf_app.py
```
 
The app opens on <http://localhost:8501>. The first display of the national map
computes every route and can take a few seconds (a progress bar is shown).
 
## Data processing
 
Raw data are cleaned in `src/core/data_preprocessing.py` before any statistic is computed.
No row is dropped: unreliable values are corrected, imputed or set to `NaN`.
 
1. COVID-19 period (March 2020 → June 2021): measures set to `NaN`.
2. Q1 2025: counts of trains delayed by more than 30 and 60 minutes set to `NaN`
   (data quality issue).
3. Mean delays that are inconsistent with the number of delayed trains are set to `NaN`
   or imputed with the historical median of the same service, route and calendar month
   (at least 2 valid observations required).
4. Inconsistent "> 15 min" counts are invalidated; small negative mean delays are
   set to 0, large ones to `NaN`.
5. Routes present twice in the same month (National and International service) are merged,
   with weighted means for delays and percentages.
6. A column `Prct retard causes non renseignées` is added so that delay causes sum to 100 %.
## Quality and tests
 
```bash
uv run ruff check .          # lint (PEP 8, imports, bugbear, pyupgrade)
uv run ruff format .         # format
uv run mypy .                # type checking
uv run pytest                # tests + coverage (configured in pyproject.toml)
```
 
- Tests rely on mocked dataframes (`tests/conftest.py`) covering COVID-period
  invalidation, delay corrections, missing-value imputation, consistency checks on delay
  counts.
- Streamlit widgets are tested with `streamlit.testing.v1.AppTest`. Code executed through
  `AppTest.from_function()` may not be counted by `coverage.py`, so the reported coverage
  can be lower than the real one.
 
## Logging
 
Logging is configured in `config/logging.conf` and initialised when the app starts:
 
| Output | Level | Destination |
| --- | --- | --- |
| Console | DEBUG and above | stdout (coloured with `colorlog`) |
| Debug file | DEBUG and above | `logs/app.log` |
| Error file | ERROR and CRITICAL | `logs/error.log` |
 
 Each new session creates a log file timestamped with creation time.

## Documentation
 
API documentation is generated by Sphinx with AutoAPI from the docstrings
(Napoleon / Google style):
 
```bash
uv run sphinx-build -b html docs docs/_build/html
```
 
Open `docs/_build/html/index.html`. On Windows, `docs\make.bat html` also works. More
details in [`docs/_other/sphinx_utilisation.md`](docs/_other/sphinx_utilisation.md).
 
## CI/CD and deployment
 
| Workflow | Trigger | What it does |
| --- | --- | --- |
| `.github/workflows/test.yaml` | every push, pull requests to `main` | Installs dependencies with `uv` and runs `pytest` |
| `.github/workflows/docker.deploy.yml` | push on `main` | Builds the Docker image (not published) |
 
The application is deployed on **Streamlit Community Cloud**, connected directly to this
repository: each push on `main` redeploys the app.
 
## Known limitations
 
- Foreign stations (Barcelona, Madrid, Zurich, Frankfurt, Stuttgart, Geneva, Lausanne,
  Italy) have no railway geometry: they are drawn up to the closest French station.
- Some routes are drawn from a hand-made mapping between route names and railway line ids
  (`src/core/railway_data/__init__.py`); a few routes may be missing on the map.
- Statistics from the COVID period are intentionally excluded.
## Glossary
 
| Term | Definition |
| --- | --- |
| `departure_station` | Station where the train starts the monthly-monitored route |
| `arrival_station` | Station where the train ends the route |
| Route / connection | An ordered pair (departure, arrival); A→B and B→A are distinct |
| Service | `National` or `International` |
| Planned trains | Number of scheduled circulations in the month |
| Cancelled trains | Number of scheduled circulations not run |
| Mean delay of delayed trains | Average delay (minutes) over late trains only |
| Mean delay of all trains | Average delay (minutes) over all trains, late or not |
| Delay cause (%) | Share of the total delay minutes attributed to a cause |
| Unknown cause (%) | `100 − sum of the six declared causes`, computed in preprocessing |
 
## Authors and licence
 
Pierre Marlier, Ulysse Perruchon-Monge, Christophe Vandenborre — Télécom Paris.
 
Data: SNCF open data, see the datasheet for the
terms of use.
 