from datetime import datetime, timedelta
import logging
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from ingest.ingest_xkcd import ingest_latest
from ingest.xkcd_sensor import create_xkcd_sensor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# DAG-level config to skip using the sensor for ad-hoc/demo runs
skip_sensor = os.getenv("SKIP_SENSOR", "True").lower() == "true"

logger.info(f"SKIP_SENSOR environment variable: {os.getenv('SKIP_SENSOR', 'Not Set')}")
logger.info(f"Skip sensor boolean: {skip_sensor}")

with DAG(
    dag_id="xkcd_pipeline",
    default_args=default_args,
    description="ETL pipeline: ingest XKCD comics and run dbt transforms and tests",
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 9 * * MON,WED,FRI",
    catchup=False,
    max_active_runs=1,
    tags=["xkcd", "data-engineering", "case-study"],
) as dag:
    # Step 0: ingest latest comic first if DB is empty
    ingest_latest_task = PythonOperator(
        task_id="ingest_latest",
        python_callable=ingest_latest,
        provide_context=True,
    )

    # Step 1: sensor
    wait_for_comic = create_xkcd_sensor(
        task_id="wait_for_today_comic",
        skip_sensor=skip_sensor,
        demo_timeout=1800,  # 30 minutes
    )

    # Step 2: run dbt models
    dbt_run = BashOperator(
        task_id="dbt_run",
        cwd="/opt/airflow/dbt",
        bash_command="dbt run --profiles-dir /opt/airflow/.dbt",
    )

    # Step 3: run dbt tests
    dbt_test = BashOperator(
        task_id="dbt_test",
        cwd="/opt/airflow/dbt",
        bash_command="dbt test --profiles-dir /opt/airflow/.dbt",
    )

    # Step 4: generate dbt documentation
    dbt_docs_generate = BashOperator(
        task_id="dbt_docs_generate",
        cwd="/opt/airflow/dbt",
        bash_command="dbt docs generate --profiles-dir /opt/airflow/.dbt",
    )

    # Task dependencies
    ingest_latest_task >> wait_for_comic >> dbt_run >> dbt_test >> dbt_docs_generate
