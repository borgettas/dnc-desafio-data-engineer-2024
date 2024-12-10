FROM apache/airflow:2.10.3-python3.9 as base
COPY requirements.txt requirements.txt

USER 50000

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
