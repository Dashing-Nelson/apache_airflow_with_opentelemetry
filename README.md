# apache_airflow_with_opentelemetry

# Introduction
This repository provides a Docker Compose configuration to set up an Apache Airflow cluster using the CeleryExecutor. It includes additional services like Redis, PostgreSQL, MySQL, Adminer, Jaeger, OpenTelemetry Collector, Prometheus, and Grafana to enhance functionality, monitoring, and tracing capabilities.

This setup is intended for local development and testing purposes. It is not recommended for production deployments. The configuration allows you to experiment with Airflow and its integrations with various monitoring and tracing tools.

# Prerequisites
Docker installed on your machine
Docker Compose installed (if not included with Docker)

# Services Overview
The Docker Compose configuration includes the following services:

# Airflow Components
- airflow-webserver: The web interface for Apache Airflow.
- airflow-scheduler: Monitors and triggers scheduled tasks.
- airflow-worker: Executes the tasks queued by the scheduler.
- airflow-triggerer: Handles deferred tasks.
- airflow-init: Initializes the Airflow environment (database migrations, user creation).
# Databases
- postgres: PostgreSQL database used by Airflow for metadata storage.
- mysql: MySQL database for testing purposes (e.g., sample datasets).
- Message Broker
- redis: In-memory data store used as a message broker for CeleryExecutor.
# Database Management
- adminer: Web-based database management tool for MySQL.
# Monitoring and Tracing
- jaeger: Distributed tracing system for microservices.
- hotrod: A sample application to generate tracing data for Jaeger.
- otel-collector: OpenTelemetry Collector to process and export telemetry data.
- prometheus: Monitoring system to collect metrics from the services.
- grafana: Analytics platform to visualize data collected by Prometheus.


# To start the container
1. Start the containers by running `docker-compose up`. wait for the process to complete
2. Go to [the Apache Airflow dashboard at localhost:8080](localhost:8080). Use `airflow` as the username and password.

# To follow the example for sending traces to Jaeger via OpenTelemetry
1. Click `etl_pipeline` DAG and run it. This should send a trace to Jaeger via OpenTelemetry
2. Go to (Jaeger UI)[http://localhost:16686/] and select `my-helloworld-service` if not selected already.
3. Click `Find Traces`. A trace should appear.

# To follow the example for sending metrics to Promethus via Otel Collector
1. The DAG `sleep_random` is scheduled to run every second. So it would already be sending tracing to Promethus
2. Go to the (Grafana UI)[http://localhost:23000/] and click the `+` button.
3. Add an empty panel.
4. Change the data source to Promethus
5. Click the `metrics browse`
6. select `airflow_dagrun_duration_success_sleep_random{}`
7. This will plot a graph which could be added to the dashboard

# License
This project is licensed under the Apache License, Version 2.0. See the LICENSE file for details.
