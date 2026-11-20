## ![Alternative text](resources/logo_sncf.png) IADATA700 - Kit Big Data Project ![Alternative text](resources/logo_tp.png)
# Streamlit Application to monitor SNCF punctuality
 
This interactive app has been built to help people understanding, and somehow gathering insights, whether a train could be canceled, delayed, and if delayed, how much delay the customer would likely has to face. 

We picked two use-case, that framed our entire application :

- one could want to overview the global railway network punctuality informations (mean delay at arrival route by route, and possible delay causes),
- one could want to setup a specific trip, with a given pair departure - destination, on a particular time frame over the year (monthly is the best available sampling)
 
All the displayed data are computed from a SNCF open dataset downloadable at https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/information/.

Project developed by Pierre Marlier, Ulysse Perruchon-Monge and Christophe Vandenborre.
 
🔗 **Live app:** meet-your-train.streamlit.app
 

---
 
# Overview
 
We wanted to find an answer to a question we asked ourselves many times : **"How likely is my train to be delayed? What ?! "20 minutes delayed" ?? What is going on this time?"**
 
So we explore the dataset under different ways:

 - Displaying the mean delay at arrival on a map 
 - Displaying the possible delay causes and their mean proportion of occurrences on a pie chart
 - Displaying the proportion of canceled and delayed train (on departure and on arrival) on a table
 - Displaying the stastical history of delay at arrival over months and years on a graph chart

We later describe quickly on what data these insights has been computed.
For more details, please check the datasheet attached to the project.

As previously mentioned, the user will gain access to two different interfaces :

- a global overview of the french railway network (with delay map and delay causes proportion)
- a trip-oriented specific dashboard (with delay history graph, delay causes proportion, cancelation/delay table and a map)
 
---

## Project structure (generated with AI)
 
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
 
The code is split in three: the `core` block that holds all the computation packages, the `ui` block that holds all the display units and finally the `streamlit_sncf_app.py` that brings everything together and holds the front end as well as the gateway between core and ui.

---

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

---
### Data
 
All the required data are embedded with the project, uploaded on GitHub. The files to be processed are CSV files expected to be found in `data/raw/`:
 
Three files are required to have full functionalities:
| File | Used for |
| --- | --- |
| `regularite-mensuelle-tgv-aqst.csv` | Monthly regularity per TGV route (main dataset) |
| `lignes-par-region-administrative.csv` | Geographical data points for every railway section (stored by SNCF internal id) over France |
| `liste-des-gares.csv` | Geographical coordinates for every railstation over France |
 
We could have plugged the website on the SNCF API, but to keep the system up even with no Internet access or in case of unavailability of the SNCF website, we'd rather setup every files locally.

To refresh data if required, the best way is to download the latest export from https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/export/
and replace it in `data/raw/` (keep the same file name). 

---
### Run the app
 
To run the app from the source code, simply type the following command: 
 
```bash
cd streamlit_sncf
uv run streamlit run src/streamlit_sncf_app.py
```
Or launch the on-line version (hosted on StreamlitCloud) by reaching `meet-your-train.streamlit.app`

---
### Quick starting guidestep

On the starting page, the two buttons underneath the title will route the user to the one of the following screen configuration, depending on your choice:

### 1) Global overview (national statistics)

Two sided-window :

- on the left, 
    - on the upper-part, a static pie chart displaying the overall delay causes proportion - we intuited the main entity responsible for each cause, based on our prior knowledge of the system,
    - on the lower-part, a small take-away panel, also static, with insights from our data analysis,

- on the right, 
    - an interactive map displaying (almost) all the railway path listed in the CSV data file ; railtracks are colored regarding their mean delay over all the data in the dataset,
    - the slider above the map sets a filter over the drawn railway : if the mean delay of the railway is between the slider values, it is drawn on the map.


### 2) Specific trip configuration

Three sided-window :

- on the sidebar,
    - this is the only interactive part of this screen configuration :
        - the user may set the departure city (the arrival list is computed from the departure, the inverse is not true...),
        - the user may pick a month range to analyze data of the given departure - arrival pair on a specific frame in a year (start month must be prior end month),
        - the user may select a year range to analyze data of the given departure - arrival pair on a specific year frame (remove year by clicking the cross or add them by picking them out of the scroll list),

        Everything is computed on the fly.

- on the main window,
    - on the left,
        - on the upper-part, a graph displaying statistics of delay (distribution, median) across a year (month division) and based on the parameters from the sidebar,
        - on the lower-part, a static pie chart displaying the overall delay causes proportion based on the parameters from the sidebar - we intuited the main entity responsible for each cause, based on our prior knowledge of the system,

  - on the right, 
        - on the upper-part, a small map displaying the colored railway path based on the parameters from the sidebar,
        - on the lower-part, a small table displaying the statistics of cancelled and delayed trains based on the parameters from the sidebar,
 
The user may switch from one screen configuration to the other one without any restriction (except maybe waiting for the -sometimes long- loading time)
 
---
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

---
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
 
---
## Logging
 
Logging is configured in `config/logging.conf` and initialised when the app starts:
 
| Output | Level | Destination |
| --- | --- | --- |
| Console | DEBUG and above | stdout (coloured with `colorlog`) |
| Debug file | DEBUG and above | `logs/app.log` |
| Error file | ERROR and CRITICAL | `logs/error.log` |
 
Each new session logs are added to the current log file until the limite size is reach.
A message "Starting new session" is added everytime the app is launched

---
## Documentation
 
API documentation is generated by Sphinx with AutoAPI from the docstrings
(Napoleon / Google style):
 
```bash
uv run sphinx-build -b html docs docs/_build/html
```
 
Open `docs/_build/html/index.html`. On Windows, `docs\make.bat html` also works. More
details in [`docs/_other/sphinx_utilisation.md`](docs/_other/sphinx_utilisation.md).
 
---
## CI/CD and deployment
 
| Workflow | Trigger | What it does |
| --- | --- | --- |
| `.github/workflows/test.yaml` | every push, pull requests to `main` | Installs dependencies with `uv` and runs `pytest` |
| `.github/workflows/docker.deploy.yml` | push on `main` | Builds the Docker image - as long as we don't have a Dockerbuild account, under the advice of our teacher, we chose the StreamlitCloud deployment, linking the app to the GitHub main branch|

 
---
## Known limitations
 
- Foreign stations (Barcelona, Madrid, Zurich, Frankfurt, Stuttgart, Geneva, Lausanne,
  Italy) have no railway geometry: they are drawn up to the closest French station.
- Some routes are drawn from a hand-made mapping between route names and railway line ids
  (`src/core/railway_data/__init__.py`); a few routes may be missing on the map.
- Statistics from the COVID period are intentionally excluded.
- Some bugs still remains
    - loading latency
    - unexpected refresh of Folium map
    - pie-chart on the "Global overview" configuration is not linked to the slider

---
## Glossary
 
| Term | Definition |
| --- | --- |
| Departure station | Station where the train starts the monthly-monitored route |
| Arrival station | Station where the train ends the route |
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
 
Data: SNCF open data, see the datasheet for the terms of use.
 