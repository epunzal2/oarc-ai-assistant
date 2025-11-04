from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.rag import telemetry


def test_sampler_backend_prefers_pynvml(monkeypatch: pytest.MonkeyPatch):
    dummy_nvml = SimpleNamespace(
        nvmlInit=lambda: None,
        nvmlShutdown=lambda: None,
        nvmlDeviceGetCount=lambda: 0,
    )
    monkeypatch.setattr(telemetry, "pynvml", dummy_nvml)
    monkeypatch.setattr(telemetry, "psutil", None)
    monkeypatch.setattr(telemetry.shutil, "which", lambda _: None)

    sampler = telemetry.TelemetrySampler()
    assert sampler.backend == "pynvml"


def test_sampler_backend_falls_back_to_psutil(monkeypatch: pytest.MonkeyPatch):
    dummy_psutil = SimpleNamespace(
        cpu_percent=lambda interval=None: 42.0,
        virtual_memory=lambda: SimpleNamespace(used=1024 * 1024 * 8),
    )
    monkeypatch.setattr(telemetry, "pynvml", None)
    monkeypatch.setattr(telemetry, "psutil", dummy_psutil)
    monkeypatch.setattr(telemetry.shutil, "which", lambda _: None)

    sampler = telemetry.TelemetrySampler()
    assert sampler.backend == "psutil"
    sample = sampler._collect_cpu_metrics()  # pylint: disable=protected-access
    assert sample["cpu.percent"] == 42.0
    assert pytest.approx(sample["memory.rss_mb"], rel=1e-3) == 8.0


def test_flush_clears_buffer(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(telemetry, "pynvml", None)
    monkeypatch.setattr(telemetry, "psutil", None)
    monkeypatch.setattr(telemetry.shutil, "which", lambda _: None)

    sampler = telemetry.TelemetrySampler()
    sampler.backend = "none"
    sampler._buffer.append({"cpu.percent": 10.0})  # pylint: disable=protected-access

    first_flush = sampler.flush()
    assert first_flush == [{"cpu.percent": 10.0}]
    assert sampler.flush() == []

