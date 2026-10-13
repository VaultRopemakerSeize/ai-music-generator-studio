"""Bootstrap: locate weights, warm the model cache, pick the audio driver.

Runs before any pipeline stage. Idempotent — safe to call from CLI, GUI, or
the C#/Java sidecar hosts.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from platformdirs import user_cache_dir

from ai_music_studio.config import settings
from ai_music_studio.services.model_registry import ModelRegistry

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Runtime:
    weights_dir: Path
    cache_dir: Path
    registry: ModelRegistry
    device: str


def bootstrap(*, force_cpu: bool = False) -> Runtime:
    """Resolve paths, load the registry, choose a device. ~40ms cold, ~3ms warm."""
    weights_dir = settings.weights_dir
    cache_dir = Path(user_cache_dir("ai-music-generator-studio"))
    cache_dir.mkdir(parents=True, exist_ok=True)

    device = "cpu"
    if not force_cpu:
        try:
            import torch

            if torch.cuda.is_available():
                device = "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                device = "mps"
        except ImportError:
            log.debug("torch not importable; staying on cpu")

    registry = ModelRegistry(weights_dir=weights_dir, cache_dir=cache_dir)
    registry.discover()
    log.info("bootstrap ok device=%s models=%d", device, len(registry))
    return Runtime(weights_dir=weights_dir, cache_dir=cache_dir, registry=registry, device=device)