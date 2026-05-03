"""Background host/GPU telemetry sampler used by instrumented RAG runs."""

from __future__ import annotations

import shutil
import subprocess
import threading
import time
from collections import deque
from typing import Any, Deque, Dict, List, Optional

from src.rag import config
from src.rag.logger import get_logger

logger = get_logger(__name__)

try:  # pragma: no cover - optional dependency
    import psutil  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    psutil = None

try:  # pragma: no cover - optional dependency
    import pynvml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pynvml = None


class TelemetrySampler:
    """Collects bounded telemetry samples without blocking request execution."""

    def __init__(self) -> None:
        self.interval = max(1.0, float(config.TELEMETRY.interval_seconds))
        self.backoff = max(self.interval, float(config.MLFLOW.sampler_backoff_seconds))
        self.timeout = max(1.0, float(config.MLFLOW.sampler_timeout_seconds))
        self._stop_event = threading.Event()
        self._buffer: Deque[Dict[str, Any]] = deque(
            maxlen=max(1, int(config.TELEMETRY.sample_window))
        )
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self.backend = self._select_backend()
        self._initialized_nvml = False

    def start(self) -> None:
        """Start the daemon sampler when telemetry is enabled and available."""

        if not config.TELEMETRY.enabled:
            return
        if self.backend == "none":
            if not config.TELEMETRY.fail_silently:
                logger.warning("No telemetry backend available.")
            return
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop,
            name="telemetry-sampler",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """Stop the sampler and release NVML if that backend was initialized."""

        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self.timeout)
        if self._initialized_nvml and pynvml is not None:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                logger.debug("Failed to shutdown NVML cleanly", exc_info=True)
            finally:
                self._initialized_nvml = False

    def flush(self) -> List[Dict[str, Any]]:
        """Return buffered samples and clear the in-memory window."""

        with self._lock:
            payload = list(self._buffer)
            self._buffer.clear()
        return payload

    def _select_backend(self) -> str:
        if config.TELEMETRY.record_gpu and pynvml is not None:
            try:
                pynvml.nvmlInit()
                self._initialized_nvml = True
                logger.debug("Telemetry sampler using pynvml backend")
                return "pynvml"
            except Exception:
                logger.debug("pynvml initialization failed", exc_info=True)
        if config.TELEMETRY.record_gpu and shutil.which("nvidia-smi"):
            logger.debug("Telemetry sampler using nvidia-smi backend")
            return "nvidia-smi"
        if psutil is not None:
            logger.debug("Telemetry sampler using psutil backend")
            return "psutil"
        logger.debug("Telemetry sampler running without backend")
        return "none"

    def _run_loop(self) -> None:
        wait_interval = self.interval
        while not self._stop_event.wait(wait_interval):
            try:
                sample = self._collect_sample()
                if sample:
                    sample["timestamp"] = time.time()
                    sample["backend"] = self.backend
                    with self._lock:
                        self._buffer.append(sample)
                wait_interval = self.interval
            except Exception:
                logger.debug("Telemetry sampling failed", exc_info=True)
                wait_interval = self.backoff

    def _collect_sample(self) -> Optional[Dict[str, Any]]:
        if self.backend == "pynvml":
            return self._collect_gpu_nvml()
        if self.backend == "nvidia-smi":
            return self._collect_gpu_nvidia_smi()
        if self.backend == "psutil":
            return self._collect_psutil()
        return None

    def _collect_gpu_nvml(self) -> Optional[Dict[str, Any]]:
        if pynvml is None:
            return None
        try:
            device_count = pynvml.nvmlDeviceGetCount()
        except Exception:
            logger.debug("nvmlDeviceGetCount failed", exc_info=True)
            return self._collect_psutil()
        if device_count == 0:
            return self._collect_psutil()
        gpu_util = []
        gpu_mem = []
        gpu_power = []
        for idx in range(device_count):
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                gpu_util.append(util.gpu)
                gpu_mem.append(memory.used / (1024 * 1024))
                try:
                    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                except Exception:
                    power = 0.0
                gpu_power.append(power)
            except Exception:
                logger.debug("Failed to sample NVML device %s", idx, exc_info=True)
        sample: Dict[str, Any] = {}
        if gpu_util:
            sample["gpu.utilization"] = sum(gpu_util) / len(gpu_util)
        if gpu_mem:
            sample["gpu.memory_mb"] = sum(gpu_mem) / len(gpu_mem)
        if gpu_power:
            sample["gpu.power_w"] = sum(gpu_power) / len(gpu_power)
        sample.update(self._collect_cpu_metrics())
        return sample

    def _collect_gpu_nvidia_smi(self) -> Optional[Dict[str, Any]]:
        command = [
            "nvidia-smi",
            "--query-gpu=utilization.gpu,memory.used,power.draw",
            "--format=csv,noheader,nounits",
        ]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=True,
            )
        except Exception:
            logger.debug("nvidia-smi command failed", exc_info=True)
            return self._collect_psutil()
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            return self._collect_psutil()
        util_vals = []
        mem_vals = []
        power_vals = []
        for line in lines:
            try:
                parts = [p.strip() for p in line.split(",")]
                util_vals.append(float(parts[0]))
                mem_vals.append(float(parts[1]))
                if len(parts) > 2:
                    power_vals.append(float(parts[2]))
            except (ValueError, IndexError):
                logger.debug("Failed to parse nvidia-smi line: %s", line)
        sample: Dict[str, Any] = {}
        if util_vals:
            sample["gpu.utilization"] = sum(util_vals) / len(util_vals)
        if mem_vals:
            sample["gpu.memory_mb"] = sum(mem_vals) / len(mem_vals)
        if power_vals:
            sample["gpu.power_w"] = sum(power_vals) / len(power_vals)
        sample.update(self._collect_cpu_metrics())
        return sample

    def _collect_psutil(self) -> Optional[Dict[str, Any]]:
        if psutil is None:
            return None
        sample = self._collect_cpu_metrics()
        return sample if sample else None

    def _collect_cpu_metrics(self) -> Dict[str, Any]:
        metrics: Dict[str, Any] = {}
        if psutil is None:
            return metrics
        try:
            metrics["cpu.percent"] = psutil.cpu_percent(interval=None)
        except Exception:
            logger.debug("psutil.cpu_percent unavailable", exc_info=True)
        try:
            mem = psutil.virtual_memory()
            metrics["memory.rss_mb"] = mem.used / (1024 * 1024)
        except Exception:
            logger.debug("psutil.virtual_memory unavailable", exc_info=True)
        return metrics


_SAMPLER: Optional[TelemetrySampler] = None


def get_sampler() -> TelemetrySampler:
    """Return the process-wide telemetry sampler."""

    global _SAMPLER
    if _SAMPLER is None:
        _SAMPLER = TelemetrySampler()
    return _SAMPLER
