from airflow.operators.empty import EmptyOperator
from datetime import date


def create_xkcd_sensor(
    task_id: str, skip_sensor: bool = True, demo_timeout: int = 3600
):
    """
    Wait for today's XKCD comic to be available (unless skipped).

    """
    if skip_sensor:
        return EmptyOperator(task_id=task_id)

    # Only import if sensor is enabled (avoids Airflow import issues)
    from airflow.providers.http.sensors.http import HttpSensor

    return HttpSensor(
        task_id=task_id,
        http_conn_id="xkcd_api",
        endpoint="info.0.json",
        method="GET",
        response_check=lambda response: (
            response.json()["day"] == str(date.today().day)
        ),
        poke_interval=60,
        timeout=demo_timeout,
        mode="reschedule",
    )
