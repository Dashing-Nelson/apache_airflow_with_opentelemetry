from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.mysql import MySQLInstrumentor
from opentelemetry.instrumentation.pymysql import PyMySQLInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


# Instrument MySQL and Requests libraries 
MySQLInstrumentor().instrument()
PyMySQLInstrumentor().instrument()


trace.set_tracer_provider(
TracerProvider(
        resource=Resource.create({SERVICE_NAME: "my-helloworld-service"})
    )
)
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4318/v1/traces",
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(otlp_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)