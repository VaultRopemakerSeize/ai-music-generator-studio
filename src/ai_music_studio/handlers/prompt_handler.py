"""Prompt ingestion: text -> JobSpec. Applies mood presets and model defaults."""

from __future__ import annotations

from ai_music_studio.config import settings
from ai_music_studio.models.job import JobSpec, Mood
from ai_music_studio.services.model_registry import ModelRegistry


class PromptHandler:
    def __init__(self, registry: ModelRegistry) -> None:
        self._registry = registry

    def build_spec(
        self,
        *,
        prompt: str,
        mood: Mood,
        seconds: int,
        seed: int | None,
        device: str,
    ) -> JobSpec:
        model_id = settings.default_model
        if model_id not in self._registry:
            fallback = self._registry.first_available()
            if fallback is None:
                raise RuntimeError("no models available — run scripts/fetch_weights.py")
            model_id = fallback

        return JobSpec(
            prompt=prompt.strip(),
            mood=mood,
            seconds=min(seconds, settings.max_seconds),
            seed=seed,
            device=device,
            model_id=model_id,
            sample_rate=settings.sample_rate,
            channels=settings.channels,
            loop=True,
        )