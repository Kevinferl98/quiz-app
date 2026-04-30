from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

from app.config import config


_provider = None


def _build_sampler():
    # Keep parent sampling decisions across service boundaries to avoid
    # partial traces when requests span multiple services.
    if config.OTEL_TRACES_SAMPLER == "parentbased_traceidratio":
        return ParentBased(TraceIdRatioBased(config.OTEL_TRACES_SAMPLER_ARG))
    if config.OTEL_TRACES_SAMPLER == "traceidratio":
        return TraceIdRatioBased(config.OTEL_TRACES_SAMPLER_ARG)
    return ParentBased(TraceIdRatioBased(1.0))


def setup_telemetry(app) -> None:
    global _provider
    if not config.OTEL_ENABLED:
        return

    resource = Resource.create(
        {
            "service.name": config.OTEL_SERVICE_NAME,
            "deployment.environment": config.ENV,
            "service.version": "1.0.0",
        }
    )

    provider = TracerProvider(resource=resource, sampler=_build_sampler())
    exporter = OTLPSpanExporter(endpoint=config.OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)
    _provider = provider


def shutdown_telemetry() -> None:
    if _provider is not None:
        # Flush pending spans before process shutdown to avoid trace loss.
        _provider.shutdown()
