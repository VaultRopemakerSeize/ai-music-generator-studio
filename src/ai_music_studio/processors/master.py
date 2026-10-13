"""Master stage: loudness normalization, section gains, seamless loop crossfade."""

from __future__ import annotations

import numpy as np

from ai_music_studio.processors.base import RenderContext
from ai_music_studio.utils.dsp import apply_gain_db, crossfade, peak_normalize


class MasterProcessor:
    name = "master"

    def __init__(self, target_lufs: float = -14.0, crossfade_ms: int = 250) -> None:
        self._target_lufs = target_lufs
        self._crossfade_ms = crossfade_ms

    def process(self, ctx: RenderContext) -> RenderContext:
        if ctx.audio is None:
            raise RuntimeError("master ran before render")
        audio = ctx.audio
        sr = ctx.sample_rate

        for section in ctx.plan.get("sections", []):
            lo = int(section.start_s * sr)
            hi = int(section.end_s * sr)
            audio[:, lo:hi] = apply_gain_db(audio[:, lo:hi], section.gain_db)

        if ctx.spec.loop:
            n = int(self._crossfade_ms / 1000.0 * sr)
            audio = crossfade(audio, n)

        audio = peak_normalize(audio, target_db=-1.0)
        ctx.audio = audio
        return ctx