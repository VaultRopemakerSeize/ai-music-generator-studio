"""Layered settings: defaults <- config/default.toml <- env AIMS_* <- CLI overrides."""

from __future__ import annotations

import os
import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    weights_dir: Path = Field(default=Path("models/weights"))
    presets_dir: Path = Field(default=Path("models/presets"))
    outputs_dir: Path = Field(default=Path("outputs"))
    sample_rate: int = Field(default=48_000, ge=8_000, le=192_000)
    channels: int = Field(default=2, ge=1, le=2)
    block_frames: int = Field(default=4096, ge=256, le=65_536)
    max_seconds: int = Field(default=600, ge=4, le=3600)
    default_model: str = Field(default="musicgen-small")
    allow_unsafe_weights: bool = False

    @classmethod
    def load(cls, path: Path | None = None) -> "Settings":
        base: dict[str, object] = {}
        toml_path = path or Path("config/default.toml")
        if toml_path.is_file():
            with toml_path.open("rb") as fh:
                base = tomllib.load(fh).get("studio", {})
        for key in cls.model_fields:
            env_key = f"AIMS_{key.upper()}"
            if env_key in os.environ:
                base[key] = os.environ[env_key]
        return cls(**base)


@lru_cache(maxsize=1)
def _cached() -> Settings:
    return Settings.load()


settings: Settings = _cached()