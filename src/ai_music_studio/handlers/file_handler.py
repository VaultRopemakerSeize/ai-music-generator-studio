"""File ingestion: drop a .txt brief or a .toml project file, get a JobSpec back."""

from __future__ import annotations

import tomllib
from pathlib import Path

from ai_music_studio.models.job import JobSpec, Mood


class FileHandler:
    """Reads project files. Never trusts paths — callers must pass resolved paths."""

    def load_project(self, path: Path) -> JobSpec:
        if not path.is_file():
            raise FileNotFoundError(path)
        with path.open("rb") as fh:
            doc = tomllib.load(fh)
        job = doc.get("job", {})
        return JobSpec(
            prompt=str(job.get("prompt", "ambient pad")),
            mood=Mood(job.get("mood", Mood.NEUTRAL)),
            seconds=int(job.get("seconds", 60)),
            seed=job.get("seed"),
            model_id=str(job.get("model_id", "musicgen-small")),
        )

    def load_brief(self, path: Path) -> str:
        return path.read_text(encoding="utf-8").strip()