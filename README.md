# Streamlit SNCF

Projet Python géré avec `uv`, avec une application Streamlit et un socle CI/CD.
Pour d'autres bonnes pratiques MLOps, suivre https://github.com/fmind/mlops-python-package

## Installation

```powershell
uv sync --dev
```

## Lancer l'application

```powershell
uv run streamlit run streamlit/streamlit_app.py
```

## Qualité et tests

```powershell
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run pytest
```

## Hooks Git locaux

```powershell
uv run pre-commit install
uv run pre-commit run --all-files
```
# Glossary

| string    | definition |
| --------- | ------- |
| departure_station |  departure station  |
| arrival_station | arrival station  |
|           |         |
|           |         |
|           |         |
|           |         |
|           |         |
