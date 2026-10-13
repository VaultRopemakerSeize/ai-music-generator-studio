"""Preset handler: named mood packs from models/presets/*.toml."""

from __future__ import annotations

import tomllib
from pathlib import Path

from ai_music_studio.config import settings
from ai_music_studio.models.job import Mood


class PresetHandler:
    def __init__(self, presets_dir: Path | None = None) -> None:
        self._dir = presets_dir or settings.presets_dir

    def list_presets(self) -> list[str]:
        if not self._dir.is_dir():
            return []
        return sorted(p.stem for p in self._dir.glob("*.toml"))

    def load(self, name: str) -> dict[str, str]:
        path = self._dir / f"{name}.toml"
        if not path.is_file():
            raise KeyError(f"unknown preset: {name}")
        with path.open("rb") as fh:
            doc = tomllib.load(fh)
        return {k: str(v) for k, v in doc.get("preset", {}).items()}

    def mood_for(self, name: str) -> Mood:
        return Mood(self.load(name).get("mood", Mood.NEUTRAL))
</｜｜DSML｜｜ parameter>