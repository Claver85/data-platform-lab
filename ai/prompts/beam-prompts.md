# Apache Beam Prompts

---

## Design Principles

All Beam/Dataflow pipelines should follow:

- metadata-driven execution
- scalable distributed processing
- immutable raw data ingestion
- observability-first design
- retry-safe behavior
- configuration externalization
- environment isolation (DEV/PRD)
- template-ready architecture

---

## Oracle Extraction Pipeline Generator

Generate an Apache Beam pipeline in Python that:

- extracts data from Oracle databases
- supports JDBC-based extraction
- handles large-scale batch ingestion
- avoids loading full datasets into memory
- partitions extraction workloads efficiently
- writes output files to Google Cloud Storage
- supports AVRO output format
- integrates with Google Cloud Dataflow
- supports external configuration files
- supports dynamic schema definitions

Requirements:
- production-ready implementation
- scalable extraction strategy
- configurable fetch size
- retry-safe behavior
- structured logging
- compatible with Python 3.11
- compatible with DataflowRunner
- optimized for high-volume tables

Include:
- pipeline options
- schema handling
- batch partitioning strategy
- observability recommendations
- error handling

---

## Beam Pipeline Generator

Generate an Apache Beam pipeline in Python that:

- reads CSV files from Google Cloud Storage
- validates schema consistency
- transforms rows into typed records
- converts data to AVRO format
- writes partitioned output files
- supports execution in Google Cloud Dataflow
- uses ValueProvider correctly
- avoids loading full datasets into memory
- supports large-scale processing

Requirements:
- production-ready code
- modular structure
- logging included
- retry-safe logic
- compatible with Python 3.11
- compatible with DataflowRunner

---

## Metadata-Driven Pipeline Prompt

Generate an Apache Beam pipeline that:
- loads execution parameters from configuration metadata
- supports dynamic schemas
- supports schema evolution
- supports environment-based behavior (DEV/PRD)
- reads input configuration from GCS or BigQuery
- dynamically resolves source and destination paths
- integrates with Airflow orchestration

Requirements:
- reusable architecture
- modular transforms
- template-ready design
- compatible with Dataflow Flex Templates

---

## Beam Performance Optimization Prompt

Analyze this Apache Beam/Dataflow pipeline.

Focus on:
- worker autoscaling
- memory usage
- shuffle bottlenecks
- hot keys
- file sharding
- parallelism
- serialization overhead
- BigQuery write performance
- BigQuery partitioning strategy
- clustering optimization
- write disposition handling
- batch loading optimization
- AVRO write optimization

Provide:
1. bottleneck analysis
2. scaling recommendations
3. memory optimization
4. throughput improvements
5. cost optimization recommendations

---

## Beam Debugging Prompt

Analyze this Apache Beam/Dataflow issue.

Focus on:
- ValueProvider misuse
- memory bottlenecks
- serialization issues
- worker scaling
- file sharding
- AVRO schema compatibility
- Dataflow template compatibility

Provide:
1. root cause analysis
2. production-safe fix
3. scalability recommendations
4. observability improvements