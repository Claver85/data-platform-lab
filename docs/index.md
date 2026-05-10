# Data Platform Lab

AI Native Data Engineering & Platform Engineering Workspace

---

## 🧭 Platform Overview

```mermaid
flowchart LR

A[Sources] --> B[Ingestion Layer]
B --> C[Processing Layer]
C --> D[Storage Layer]
D --> E[Analytics Layer]
E --> F[Consumption]

subgraph Sources
Oracle[(Oracle DB)]
Files[(Files / APIs)]
end

subgraph Processing
Beam[Apache Beam]
Dataflow[GCP Dataflow]
Composer[Airflow / Composer]
end

subgraph Storage
GCS[Cloud Storage]
BQ[BigQuery]
end

subgraph Consumption
BI[Looker]
Dash[Dashboards]
end

Oracle --> Beam
Files --> Beam
Beam --> Dataflow
Composer --> Dataflow
Dataflow --> GCS
GCS --> BQ
BQ --> BI
BQ --> Dash