Installation
============================
Prerequisites
-------------
- Python 3.12 or later (see .python-version)
- uv (pip install uv)

Install
-------
Run the following commands to import the project from the distant repo:

.. code-block:: bash
    
    git clone https://github.com/pmarlier/streamlit_sncf.git
    cd streamlit_sncf
    uv sync --dev

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