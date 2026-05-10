---
# Physical Implementation (L2 - GCP)

---

## Ingestion

- Apache Beam pipelines
- Dataflow execution (batch mode)
- JDBC extraction from Oracle
- API ingestion services

---

## Orchestration

- Cloud Composer (Airflow)
- DAG scheduling
- Retry / backfill mechanisms

---

## Storage

| Layer | Tech | Purpose |
|------|------|--------|
| Raw | Cloud Storage | Landing zone |
| Warehouse | BigQuery | Analytics |

---

## Analytics

- Looker semantic layer
- KPI definitions
- Business dashboards

---

## Cross-cutting concerns

- IAM security model
- Cloud KMS encryption
- Logging + monitoring
- CI/CD via GitHub Actions