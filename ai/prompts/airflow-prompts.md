# Airflow Prompts

---

## DAG Generator

Generate a production-ready Apache Airflow DAG that:

- triggers a Dataflow pipeline
- validates upstream dependencies
- supports retries and alerts
- logs execution metadata
- uses environment-based configuration
- separates DEV and PRD behavior
- follows Composer best practices

Requirements:
- modular tasks
- idempotent behavior
- clean retry handling
- scalable design
- Airflow 2 compatible

---

## DAG Debugging Prompt

Analyze this Airflow DAG issue.

Focus on:
- dependency management
- retries
- deadlocks
- scheduler issues
- Composer limitations
- task parallelism
- logging failures

Provide:
1. root cause
2. fix
3. monitoring recommendations
4. scalability improvements