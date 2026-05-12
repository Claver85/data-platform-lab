# CONTEXT.md — Insurance Data Platform

> Archivo de entrada para modelos de IA.
> Pegar siempre junto con la tarea específica del módulo a desarrollar.
> No incluir código de otros módulos — solo las interfaces (firmas de funciones).

---

## Stack

| Component | Technology |
|-----------|-----------|
| Cloud | GCP |
| Orchestration | Cloud Composer 2 / Airflow 2.x |
| Processing heavy | GCP Dataflow Serverless / Apache Beam Python SDK |
| Processing light | Airflow Python operators |
| Storage raw | Cloud Storage — Avro, partitioned by fecha_lote |
| Storage warehouse | BigQuery — native tables |
| Secrets | GCP Secret Manager |
| Analytics | Looker |
| CI/CD | GitHub Actions |
| Python | 3.11, type hints obligatorios, docstrings en inglés |

---

## Data Layer Pattern

Every entity follows exactly this sequence:

```
raw_{entidad}   → Avro to GCS (fecha_lote=YYYY-MM-DD/)
his_{entidad}   → INSERT INTO BQ history table (partitioned by fecha_lote)
act_{entidad}   → MERGE/UPSERT BQ active table (by PK from aud_columna)
```

- Raw: immutable Avro, never modified after write
- History: append-only, one partition per daily batch
- Active: latest version per record, identified by PK natural

---

## Orchestration Pattern

```
cad_{source}                          # Chain DAG — triggers groups sequentially
  └── dag_grupo_{source}_{nn}         # Group DAG — runs models in parallel
        ├── raw_entidad_1 → his_entidad_1 → act_entidad_1
        └── raw_entidad_2 → his_entidad_2 → act_entidad_2
```

- Chain DAG reads DAG name → queries `aud_modelo` → builds sequential TriggerDagRunOperators
- Group DAG reads DAG name → queries `aud_entidad` → builds parallel task chains
- Order within chain and group defined by `aud_dependencia`

---

## Framework Module — Entry Point

Every DAG does:
```python
from framework import build_dag
dag = build_dag(dag_name=__name__, schedule=...)
```

`build_dag` resolves everything: reads `aud_*`, selects operators, generates tasks.

---

## Config File — `{modelo}.config` on GCS

The framework generates this file before any extraction. It is the contract between
Airflow (control plane) and Dataflow (execution plane).

```json
{
  "modelo": "string",
  "fecha_lote": "YYYY-MM-DD",
  "source": {
    "type": "oracle|postgresql|mysql|sqlserver|api_salesforce|api_rest|csv|pdf",
    "connection": { "secret_ref": "projects/.../secrets/..." },
    "query": "SELECT ... resolved from aud_columna",
    "extraction_mode": "full|incremental"
  },
  "avro_schema": { "...": "built from aud_columna" },
  "destination": { "gcs_path": "gs://...", "format": "avro" },
  "validations": [ { "type": "...", "severity": "error|warning" } ]
}
```

Dataflow reads this file and needs no access to aud_* tables.

---

## aud_* Tables — Quick Reference

| Table | Purpose | Key fields |
|-------|---------|-----------|
| `aud_modelo` | Domain grouping, chain assignment | `modelo_id`, `chain_dag`, `is_active` |
| `aud_entidad` | One row per extracted entity | `source_type`, `executor_type`, `extraction_mode` |
| `aud_columna` | Schema + PK + query columns | `es_pk`, `tipo_dato`, `incluir_extraccion` |
| `aud_dependencia` | Execution order within chain/group | `entidad_id`, `entidad_dependiente_id`, `orden` |
| `aud_calendario` | Schedule + group/chain assignment | `grupo_dag`, `chain_dag`, `orden_en_cadena` |
| `aud_validacion` | Pre/post validation rules | `tipo_validacion`, `momento`, `severidad` |
| `aud_conexion` | Source connection metadata | `source_type`, `environment`, `secret_ref` |
| `aud_ejecucion` | Execution audit log (written by framework) | `estado`, `rows_extracted`, `fecha_ejecucion` |

---

## Framework Library Structure

```
libs/
├── framework/
│   ├── dag_builder.py        # build_dag() — entry point, reads DAG name
│   ├── config_builder.py     # builds {modelo}.config from aud_* tables
│   ├── config_uploader.py    # uploads config to GCS
│   ├── task_graph.py         # builds Airflow task graph from EntityConfig list
│   ├── validators.py         # evaluates aud_validacion rules
│   └── audit_writer.py       # writes to aud_ejecucion
├── operators/
│   ├── base_operator.py      # abstract base — all operators implement this
│   ├── oracle_operator.py
│   ├── postgres_operator.py
│   ├── mysql_operator.py
│   ├── sqlserver_operator.py
│   ├── salesforce_operator.py
│   ├── rest_api_operator.py
│   ├── file_operator.py
│   ├── pdf_operator.py
│   └── dataflow_operator.py  # triggers Dataflow job, passes config path
├── loaders/
│   ├── bq_history_loader.py  # INSERT INTO history partition
│   └── bq_active_merger.py   # MERGE into active by PK
└── models/
    ├── entity_config.py      # EntityConfig dataclass
    ├── pipeline_config.py    # full {modelo}.config dataclass
    └── validation_result.py  # ValidationResult dataclass
```

---

## Critical Interfaces

```python
# dag_builder.py
def build_dag(dag_name: str, schedule: str, default_args: dict) -> DAG: ...

# config_builder.py
def build_pipeline_config(entity: EntityConfig, fecha_lote: date) -> PipelineConfig: ...

# operators/base_operator.py
class BaseExtractOperator(BaseOperator):
    def execute(self, context: Context) -> ExtractResult: ...

# loaders/bq_history_loader.py
def load_to_history(entity: EntityConfig, fecha_lote: date) -> LoadResult: ...

# loaders/bq_active_merger.py
def merge_to_active(entity: EntityConfig, fecha_lote: date) -> MergeResult: ...

# validators.py
def run_validations(entity: EntityConfig, momento: str, context: dict) -> ValidationResult: ...
```

---

## Conventions

- DAG naming: `cad_{source}` / `dag_grupo_{source}_{nn}`
- Task naming: `raw_{entidad}` / `his_{entidad}` / `act_{entidad}`
- GCS raw path: `gs://{env}-{project}-raw/{modelo}/{entidad}/fecha_lote={YYYY-MM-DD}/`
- GCS config path: `gs://{env}-{project}-configs/{modelo}_{fecha_lote}.config`
- BQ datasets: `{modelo}_history` / `{modelo}_active`
- All logs include `entity_id` and `fecha_lote` as structured labels
- Credentials: never hardcoded, always via GCP Secret Manager ref
- Type hints obligatorios
- Docstrings en inglés
- Tests unitarios con pytest, mocks para BQ / GCS / source DBs
