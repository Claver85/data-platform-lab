# Orquestador Dinámico por Metadatos

## 1. Diseño de la Tabla de Configuración (BigQuery)
Para evitar hardcodear variables, Airflow leerá de una tabla de control.

```mermaid
erDiagram
    PIPELINE_CONFIG {
        string table_id PK "Ej: 'clientes', 'polizas'"
        string source_type "Ej: 'oracle_onprem', 'api'"
        string extraction_mode "Ej: 'full', 'incremental_date'"
        string dataflow_template "Ruta en GCS del template"
        string destination_raw "Dataset y tabla en BQ"
        boolean is_active "Bandera de ejecución"
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