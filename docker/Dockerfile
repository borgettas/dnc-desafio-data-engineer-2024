FROM apache/airflow:2.10.3-python3.9 as base
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml

# USER root

USER 50000
# RUN --mount=type=cache,target=/root/.cache \
#   pip install "poetry==1.6.1"

# RUN poetry install --no-interaction --no-ansi
RUN pip install --no-cache-dir -r requirements.txt