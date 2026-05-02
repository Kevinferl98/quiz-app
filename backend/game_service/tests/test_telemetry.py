from types import SimpleNamespace
from unittest.mock import MagicMock
from app import telemetry

def test_build_sampler_parentbased(monkeypatch):
    monkeypatch.setattr(telemetry.config, "OTEL_TRACES_SAMPLER", "parentbased_traceidratio")
    monkeypatch.setattr(telemetry.config, "OTEL_TRACES_SAMPLER_ARG", 0.5)

    sampler = telemetry._build_sampler()

    assert sampler is not None
    assert sampler.__class__.__name__ == "ParentBased"

def test_build_sampler_traceidratio(monkeypatch):
    monkeypatch.setattr(telemetry.config, "OTEL_TRACES_SAMPLER", "traceidratio")
    monkeypatch.setattr(telemetry.config, "OTEL_TRACES_SAMPLER_ARG", 0.25)

    sampler = telemetry._build_sampler()

    assert sampler is not None
    assert sampler.__class__.__name__ == "TraceIdRatioBased"

def test_build_sampler_fallback(monkeypatch):
    monkeypatch.setattr(telemetry.config, "OTEL_TRACES_SAMPLER", "unknown")

    sampler = telemetry._build_sampler()

    assert sampler is not None
    assert sampler.__class__.__name__ == "ParentBased"

def test_setup_telemetry_noop_when_disabled(monkeypatch):
    monkeypatch.setattr(telemetry.config, "OTEL_ENABLED", False)
    instrument_mock = MagicMock()
    monkeypatch.setattr(telemetry.FastAPIInstrumentor, "instrument_app", instrument_mock)

    telemetry.setup_telemetry(app=SimpleNamespace())

    instrument_mock.assert_not_called()

def test_setup_and_shutdown_telemetry(monkeypatch):
    monkeypatch.setattr(telemetry.config, "OTEL_ENABLED", True)
    monkeypatch.setattr(telemetry.config, "OTEL_SERVICE_NAME", "quiz_service")
    monkeypatch.setattr(telemetry.config, "ENV", "testing")
    monkeypatch.setattr(telemetry.config, "OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4317")
    monkeypatch.setattr(telemetry, "_provider", None)

    resource_create = MagicMock(return_value="resource")
    provider = MagicMock()
    tracer_provider_cls = MagicMock(return_value=provider)
    exporter_cls = MagicMock(return_value="exporter")
    span_processor_cls = MagicMock(return_value="processor")
    set_tracer_provider = MagicMock()
    instrument_app = MagicMock()

    monkeypatch.setattr(telemetry.Resource, "create", resource_create)
    monkeypatch.setattr(telemetry, "TracerProvider", tracer_provider_cls)
    monkeypatch.setattr(telemetry, "OTLPSpanExporter", exporter_cls)
    monkeypatch.setattr(telemetry, "BatchSpanProcessor", span_processor_cls)
    monkeypatch.setattr(telemetry.trace, "set_tracer_provider", set_tracer_provider)
    monkeypatch.setattr(telemetry.FastAPIInstrumentor, "instrument_app", instrument_app)

    app = SimpleNamespace()
    telemetry.setup_telemetry(app)

    resource_create.assert_called_once()
    tracer_provider_cls.assert_called_once()
    exporter_cls.assert_called_once_with(endpoint="http://tempo:4317", insecure=True)
    span_processor_cls.assert_called_once_with("exporter")
    provider.add_span_processor.assert_called_once_with("processor")
    set_tracer_provider.assert_called_once_with(provider)
    instrument_app.assert_called_once_with(app)

    telemetry.shutdown_telemetry()
    provider.shutdown.assert_called_once()
