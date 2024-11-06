# apache_airflow_with_opentelemetry

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



