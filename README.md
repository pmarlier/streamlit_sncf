# Streamlit SNCF

Python project managed with `uv`, featuring a Streamlit application and a CI/CD pipeline.

For additional MLOps best practices, please refer to the [fmind/mlops-python-package](https://github.com/fmind/mlops-python-package) project.

## Environment syncronization

```powershell
uv sync --dev
```

## Run the Application

```powershell
uv run streamlit run streamlit/streamlit_app.py
```

## Code Testing

- The tests rely on mocked_df synthetic datasets designed to cover:

    - COVID-period invalidation
    - delay statistics correction
    - missing value imputation
    - consistency checks on delay counts
    - feature engineering

- Be aware that code executed through `AppTest.from_function()` may not be
counted by coverage.py, resulting in lower reported coverage despite
successful test execution.

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