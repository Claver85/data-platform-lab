# Data Platform Architecture

## Objetivo

Procesar datos desde múltiples fuentes hacia una plataforma analítica en GCP.

---

## Flujo Principal

```mermaid
flowchart LR

Oracle --> Composer
Composer --> Dataflow
Dataflow --> CloudStorage
CloudStorage --> BigQuery
BigQuery --> Analytics
```

---

## Componentes

### Oracle
Fuente transaccional principal.

### Composer
Orquestación de pipelines y automatización.

### Dataflow
Procesamiento distribuido con Apache Beam.

### Cloud Storage
Landing y almacenamiento intermedio.

### BigQuery
Data warehouse analítico.