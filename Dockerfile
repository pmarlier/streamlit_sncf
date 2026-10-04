FROM python:3.12-slim  
WORKDIR /streamlit_sncf
RUN pip install uv
# Disable development dependencies
ENV UV_NO_DEV=1
# needed to first copy only pyproject.toml and  uv.lock
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . /streamlit_sncf
CMD ["uv", "run", "streamlit", "run", "/streamlit_sncf/src/streamlit_sncf_app.py"]