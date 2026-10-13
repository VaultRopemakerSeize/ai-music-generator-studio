"""Render stage: dispatch to the model service, get raw float32 audio back."""

from __future__ import annotations

import logging

import numpy as np

from ai_music_studio.processors.base import RenderContext
from ai_music_studio.services.generation_service import GenerationService

log = logging.getLogger(__name__)


class RenderProcessor:
    name = "render"

    def __init__(self, service: GenerationService) -> None:
        self._service = service

    def process(self, ctx: RenderContext) -> RenderContext:
        plan = ctx.plan
        audio = self._service.generate(
            prompt=plan["normalized_prompt"],
            seconds=ctx.spec.seconds,
            seed=ctx.spec.seed,
            model_id=ctx.spec.model_id,
            device=ctx.spec.device,
        )
        if audio.ndim == 1:
            audio = np.stack([audio, audio], axis=0)
        ctx.audio = audio.astype(np.float32, copy=False)
        ctx.sample_rate = ctx.spec.sample_rate
        log.info("rendered %s frames=%d", ctx.spec.cache_key(), audio.shape[-1])
        return ctx