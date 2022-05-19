# type: ignore
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from core import config


def configure_tracer() -> None:
    """Congigures opentelemetry."""
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: 'movies-api'})
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=config.JAEGER_REPORTING_HOST,
                agent_port=config.JAEGER_REPORTING_PORT,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
