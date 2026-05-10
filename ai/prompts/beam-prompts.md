# Apache Beam Prompts

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