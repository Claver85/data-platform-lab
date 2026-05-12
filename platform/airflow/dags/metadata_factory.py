"""
Minimal metadata-driven DAG factory for Airflow + Dataflow (DataflowTemplatedJobStartOperator).

Goals:
- Typed, Python 3.11
- Dataclasses-based PipelineConfig
- Mock configuration loader
- create_dag(config) factory
- Structured logging via LoggerAdapter
- Support DEV/PRD
- Minimal, modular, ready for extension

Notes:
- Keep implementation small and explicit; expand later with secrets/config backends.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator


# Expose a small public surface
__all__ = ["PipelineConfig", "load_mock_config", "create_dag"]


# --- Logging helpers -------------------------------------------------

def get_logger(name: str, extra: Optional[Dict[str, Any]] = None) -> logging.LoggerAdapter:
    """Return a structured logger adapter that will include extra contextual fields.

    Uses stdlib logging so no extra runtime dependency is required. Consumers can
    replace with structlog or other structured logging in the future.
    Ensures a default handler exists for interactive runs.
    """
    logger = logging.getLogger(name)
    # Ensure a handler exists when running outside a configured logging setup
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    if extra is None:
        extra = {}
    return logging.LoggerAdapter(logger, extra)


# --- Pipeline configuration model ------------------------------------

@dataclass
class PipelineConfig:
    """Configuration model for a pipeline DAG and Dataflow job.

    Keep the model small and explicit; extend with credentials/secret refs later.
    """

    name: str
    env: str = "DEV"  # expected values: 'DEV' or 'PRD'
    schedule: Optional[str] = None
    template_path: str = "gs://my-bucket/templates/example-template"
    region: Optional[str] = "us-central1"
    project: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    max_workers: Optional[int] = None

    def dag_id(self) -> str:
        """Return a stable DAG id derived from name and environment."""
        return f"{self.name}_{self.env.lower()}"

    def validate(self) -> None:
        """Basic validation of required fields.

        Raises ValueError for missing or invalid configuration values.
        """
        if not self.name:
            raise ValueError("PipelineConfig.name must be set")
        if self.env not in {"DEV", "PRD"}:
            raise ValueError("PipelineConfig.env must be 'DEV' or 'PRD'")
        if not self.template_path:
            raise ValueError("PipelineConfig.template_path must be set")


# --- Mock configuration loader --------------------------------------

def load_mock_config(name: str, env: str = "DEV") -> PipelineConfig:
    """Return a minimal PipelineConfig for the given name and environment.

    This is a stand-in for a real config loader (S3/GCS/DB/ConfigService) and
    provides sane defaults for local development and CI testing.
    """
    # Normalize env
    env_up = (env or "DEV").upper()
    if env_up not in {"DEV", "PRD"}:
        raise ValueError("env must be 'DEV' or 'PRD'")

    # Example per-environment overrides
    if env_up == "DEV":
        template = "gs://my-bucket/dev-templates/example-template"
        schedule = None  # manual / triggered in DEV
        project = "my-dev-project"
    else:
        template = "gs://my-bucket/prd-templates/example-template"
        schedule = "@daily"
        project = "my-production-project"

    parameters = {
        "env": env_up,
        "stagingLocation": f"gs://my-bucket/{env_up.lower()}/staging",
    }

    return PipelineConfig(
        name=name,
        env=env_up,
        schedule=schedule,
        template_path=template,
        region="us-central1",
        project=project,
        parameters=parameters,
        max_workers=5 if env_up == "DEV" else 50,
    )


# --- DAG factory -----------------------------------------------------

def create_dag(config: PipelineConfig) -> DAG:
    """Create an Airflow DAG for the provided PipelineConfig.

    The DAG contains a single DataflowTemplatedJobStartOperator task that
    launches a templated Dataflow job. Keep the DAG minimal; extend later
    to support pre/post steps, sensors, and complex control-plane logic.
    """
    # Validate config early to fail fast in CI or import-time checks
    config.validate()

    logger = get_logger(__name__, extra={"pipeline": config.name, "env": config.env})
    logger.info("Creating DAG", extra={"dag_id": config.dag_id()})

    # Basic DAG defaults — keep production-ready defaults (retries, owner)
    default_args: Dict[str, Any] = {
        "owner": "data-platform",
        "depends_on_past": False,
        "start_date": datetime(2023, 1, 1),
        "retries": 1,
    }

    dag = DAG(
        dag_id=config.dag_id(),
        default_args=default_args,
        schedule_interval=config.schedule,
        catchup=False,
        tags=["dataflow", "metadata-driven", config.env.lower()],
    )

    # Build Dataflow job parameters; keep a copy of config.parameters but ensure
    # common fields are present.
    job_parameters: Dict[str, Any] = dict(config.parameters)
    if "project" not in job_parameters and config.project:
        job_parameters["project"] = config.project
    if "region" not in job_parameters and config.region:
        job_parameters["region"] = config.region
    if config.max_workers is not None:
        job_parameters.setdefault("maxNumWorkers", str(config.max_workers))

    # Task id scoped to pipeline
    task_id = "start_dataflow"

    # Create the Dataflow Templated Job operator
    start = DataflowTemplatedJobStartOperator(
        task_id=task_id,
        template=config.template_path,
        job_name=f"{config.name}-{{{{ ds_nodash }}}}-{config.env.lower()}",
        parameters=job_parameters,
        location=config.region,
        project_id=config.project,
        dag=dag,
    )

    # Simple instrumentation
    logger.info("DAG created", extra={"tasks": [t.task_id for t in dag.tasks]})

    # Return the DAG object so callers can register it with globals() or the
    # Airflow importer.
    return dag


# --- Example usage for local development -----------------------------
# This pattern allows importing this module in Airflow: a separate loader
# script can call load_mock_config and register the returned DAGs into the
# module globals for Airflow to discover.

def _example_register():
    cfg = load_mock_config("example_pipeline", env="DEV")
    dag = create_dag(cfg)
    globals()[dag.dag_id] = dag


# When executed as a module during local dev, don't auto-register. Keep
# registration explicit to avoid surprising behavior in production imports.
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _example_register()