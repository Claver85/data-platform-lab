# Logical Architecture (L1)

```mermaid
flowchart LR

Oracle[(Oracle DB)] --> Beam[Apache Beam]
APIs[(APIs)] --> Beam
Files[(Files)] --> Beam

Beam --> Dataflow[GCP Dataflow]

Dataflow --> GCS[Cloud Storage]
GCS --> BQ[BigQuery]

BQ --> Looker[Looker]
Looker --> Dashboards[Dashboards]