"""Processor ABC and the mutable context threaded through the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np

from ai_music_studio.models.job import JobSpec


@dataclass(slots=True)
class RenderContext:
    """Mutable state carried between stages. One per job."""

    spec: JobSpec
    plan: dict[str, Any] = field(default_factory=dict)
    audio: np.ndarray | None = None
    sample_rate: int = 48_000
    warnings: list[str] = field(default_factory=list)


class Processor(Protocol):
    name: str

    def process(self, ctx: RenderContext) -> RenderContext: ...