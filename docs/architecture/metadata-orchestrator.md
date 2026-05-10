# Metadata-Driven Pipeline Orchestrator
Arquitectura de orquestación dinámica basada en metadatos para pipelines de datos sobre GCP.

## Objetivo
Centralizar y desacoplar la configuración de pipelines para permitir:

- escalabilidad operativa
- reducción de DAGs hardcodeados
- incorporación rápida de nuevas entidades
- reutilización de templates Dataflow
- estandarización de observabilidad y monitoreo

La plataforma utilizará una arquitectura metadata-driven donde Airflow actuará como plano de control (control plane) y Dataflow como plano de ejecución (execution plane).

## Arquitectura Conceptual

La plataforma se divide en dos capas principales:

| Layer | Responsabilidad |
|------|----------------|
| Control Plane | Orquestación, metadata, configuración y monitoreo |
| Execution Plane | Ejecución distribuida de pipelines y procesamiento de datos |

Airflow/Composer actuará como capa de control, mientras que Dataflow ejecutará los pipelines desacoplados de la lógica de orquestación.


## 1. Diseño de la Tabla de Configuración (BigQuery)
Para evitar hardcodear variables, Airflow leerá de una tabla de control.

```mermaid
erDiagram
    PIPELINE_CONFIG {

        string pipeline_id PK
        string config_version
        string table_id
        string source_type
        string extraction_mode

        string dataflow_template
        string destination_raw

        string schedule
        string environment

        boolean dq_enabled
        boolean is_active

        string owner_team
        string owner_email

        int max_retries
        int expected_runtime_minutes

        timestamp created_at
        timestamp updated_at
    }
```

## 2. Patrón de Diseño en Airflow (Factory)
En lugar de un script monolítico, usaremos el patrón Factory para instanciar los DAGs en base a la configuración leída.

```mermaid
classDiagram
    class ConfigFetcher {
        +get_active_pipelines() List~Dict~
    }
    class DagFactory {
        +create_dag(config: Dict) DAG
        -build_dataflow_task(config) Task
        -build_bq_sensor_task(config) Task
    }
    class PipelineConfig {
        +table_id: str
        +source_type: str
        +extraction_mode: str
    }

    ConfigFetcher --> PipelineConfig : returns
    DagFactory ..> PipelineConfig : uses
```

## 3. Flujo Operacional

```mermaid
flowchart LR

Config[PIPELINE_CONFIG] --> Composer[Composer Factory DAG]

Composer --> Validation[Config Validation]

Validation --> Trigger[Trigger Dataflow Template]

Trigger --> Beam[Apache Beam Pipeline]

Beam --> Raw[GCS Raw Layer]

Raw --> BQ[BigQuery]

Composer --> Audit[Audit Tables]
Composer --> Monitoring[Monitoring & Alerts]
```

## 4. Estrategia de Escalabilidad

La plataforma busca minimizar la creación manual de DAGs y pipelines específicos.

Nuevas entidades podrán incorporarse mediante inserciones en la tabla `PIPELINE_CONFIG`, reutilizando templates y lógica compartida.

Beneficios:

- menor costo de mantenimiento
- onboarding más rápido
- comportamiento estandarizado
- observabilidad homogénea
- desacople entre configuración y ejecución

## 5. Estrategia de Observabilidad

La plataforma centralizará métricas operativas y logs para garantizar trazabilidad end-to-end.

Capacidades esperadas:

- monitoreo de jobs Dataflow
- tracking de DAGs en Composer
- auditoría de ejecuciones
- métricas de latencia
- alertas automáticas
- detección de fallos y retries

La observabilidad será considerada un componente nativo de la plataforma y no una capacidad agregada posteriormente.

## 6. Evolución Futura

Posibles extensiones:

- integración con Data Catalog
- soporte streaming (Pub/Sub)
- lineage automático
- data contracts
- policy-based orchestration
- integración con Terraform
- self-service onboarding de pipelines

