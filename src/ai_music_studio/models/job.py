"""Core data models. Frozen where possible so pipeline stages can't mutate specs mid-flight."""

from __future__ import annotations

import hashlib
from enum import StrEnum
from pathlib import Path

import numpy as np
from pydantic import BaseModel, ConfigDict, Field


class Mood(StrEnum):
    CALM = "calm"
    FOCUS = "focus"
    TENSE = "tense"
    UPLIFT = "uplift"
    MELANCHOLY = "melancholy"
    NEUTRAL = "neutral"


class JobSpec(BaseModel):
    """Immutable description of a render. Hash-stable for cache keys."""

    model_config = ConfigDict(frozen=True)

    prompt: str = Field(min_length=1, max_length=512)
    mood: Mood = Mood.NEUTRAL
    seconds: int = Field(ge=4, le=3600)
    seed: int | None = None
    device: str = "cpu"
    model_id: str = "musicgen-small"
    sample_rate: int = 48_000
    channels: int = 2
    loop: bool = True

    def cache_key(self) -> str:
        payload = f"{self.prompt}|{self.mood}|{self.seconds}|{self.seed}|{self.model_id}".encode()
        return hashlib.blake2b(payload, digest_size=16).hexdigest()


class RenderResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    samples: np.ndarray = Field(description="float32, shape (channels, frames)")
    sample_rate: int
    spec: JobSpec

    @property
    def duration_s(self) -> float:
        return self.samples.shape[-1] / self.sample_rate

    def write(self, path: Path) -> None:
        import soundfile as sf

        path.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(path), self.samples.T, self.sample_rate, subtype="PCM_24")