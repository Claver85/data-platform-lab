# Data Platform Architecture

AI-native data platform built on GCP principles for scalable ingestion, processing, storage, and analytics.

---

## 🧭 Architecture Overview (L0 - Business View)

```mermaid
flowchart LR

Sources --> Ingestion --> Processing --> Storage --> Analytics --> Consumption

Sources[Data Sources]
Ingestion[Ingestion Layer]
Processing[Processing Layer]
Storage[Storage Layer]
Analytics[Analytics Layer]
Consumption[Business Consumption]
```

## 🏗 L1 - Logical Architecture (Platform View)

```mermaid
flowchart LR

subgraph Sources
Oracle[(Oracle DB)]
APIs[(External APIs)]
Files[(Batch Files)]
end

subgraph Ingestion Layer
Beam[Apache Beam]
Dataflow[GCP Dataflow]
end

subgraph Orchestration
Composer[Airflow / Cloud Composer]
end

subgraph Storage Layer
GCS[Cloud Storage - Raw Zone]
BQ[BigQuery - Data Warehouse]
end

subgraph Analytics Layer
Looker[Looker Semantic Layer]
end

subgraph Consumption
Dashboards[BI Dashboards]
DataApps[Data Applications]
end

Oracle --> Beam
APIs --> Beam
Files --> Beam

Composer --> Dataflow
Beam --> Dataflow

Dataflow --> GCS
GCS --> BQ

BQ --> Looker
Looker --> Dashboards
Looker --> DataApps
```