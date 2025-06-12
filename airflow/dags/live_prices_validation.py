import datetime

import zoneinfo
from airflow_alerter import AlertKind, get_teams_callbacks
from kubernetes.client import models as k8s

from airflow import DAG
from airflow.kubernetes.secret import Secret
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

local_tz = zoneinfo.ZoneInfo("Europe/Paris")

LIVE_PRICES_VALIDATION_IMG = Variable.get("__IMAGE_LIVE_PRICES_VALIDATION")
PULL_POLICY = Variable.get("__DEFAULT_PULL_POLICY", default_var=None)
NAMESPACE = Variable.get("__DEFAULT_K8S_NAMESPACE", default_var="default")
LOG_LEVEL = "DEBUG"

container_resources = k8s.V1ResourceRequirements(
    requests={"memory": "1000Mi", "cpu": "250m"},
    limits={"memory": "1000Mi", "cpu": "250m"},
)

secrets = [
    Secret("env", None, "live-prices-validation-secret")
]

LABELS = {
    "project": "live-prices-validation",
    "run_id": "{{ run_id | replace('.', '_') | replace(':', '_') | replace('+', '_') }}",
    "squad": "geckos",
}

default_args = {
    "owner": "geckos",
    "depends_on_past": False,
    "start_date": datetime.datetime(2025, 6, 12, tzinfo=local_tz),
    "params": {}
}

with DAG(
    "live_prices_validation",
    default_args=default_args,
    schedule_interval="55 9 * * 2,3,4,5,6",
    description="Retrieve live prices from Thot and send them to Teams",
    access_control={
        "geckos": {"can_read", "can_edit", "can_delete"},
    },
    catchup=False,
) as dag:
    start = DummyOperator(task_id="live_prices_validation_start")

    arguments = []

    live_prices_validation_operator = KubernetesPodOperator(
        namespace=NAMESPACE,
        image=LIVE_PRICES_VALIDATION_IMG,
        arguments=arguments,
        labels={"lang": "python", **LABELS},
        name="live_prices_validation_operator",
        task_id="live_prices_validation_operator",
        get_logs=True,
        log_events_on_failure=True,
        is_delete_operator_pod=True,
        image_pull_policy=PULL_POLICY,
        secrets=[*secrets],
        container_resources=container_resources,
        retries=0,
        startup_timeout_seconds=240,
        kubernetes_conn_id="kubernetes"
    )

    end = DummyOperator(task_id="live_prices_validation_end")

    start >> live_prices_validation_operator >> end
