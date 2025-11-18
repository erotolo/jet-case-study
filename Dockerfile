FROM apache/airflow:2.10.0-python3.11

USER root

# Install system dependencies needed for dbt + psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         build-essential \
         libpq-dev \
         curl \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python dependencies including dbt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy dbt project (source-controlled)
COPY --chown=airflow:airflow transform/xkcd_dbt/ /opt/airflow/dbt/

# Install dbt packages
WORKDIR /opt/airflow/dbt
RUN dbt deps --log-level warn

# Copy ingestion + database code
COPY --chown=airflow:airflow ingest/ /opt/airflow/ingest/
COPY --chown=airflow:airflow db/ /opt/airflow/db/

WORKDIR /opt/airflow
ENV PYTHONPATH="/opt/airflow"

HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
