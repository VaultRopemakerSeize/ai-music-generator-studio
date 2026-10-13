"""Analyze stage: normalize the prompt, infer tempo/key from mood + text cues."""

from __future__ import annotations

import re

from ai_music_studio.models.job import Mood
from ai_music_studio.processors.base import RenderContext

_BPM_BY_MOOD: dict[Mood, int] = {
    Mood.CALM: 72,
    Mood.FOCUS: 84,
    Mood.TENSE: 128,
    Mood.UPLIFT: 118,
    Mood.MELANCHOLY: 66,
    Mood.NEUTRAL: 96,
}

_KEY_BY_MOOD: dict[Mood, str] = {
    Mood.CALM: "D major",
    Mood.FOCUS: "A minor",
    Mood.TENSE: "F phrygian",
    Mood.UPLIFT: "G major",
    Mood.MELANCHOLY: "B minor",
    Mood.NEUTRAL: "C major",
}

_BPM_PAT = re.compile(r"\b(\d{2,3})\s?bpm\b", re.IGNORECASE)


class AnalyzeProcessor:
    name = "analyze"

    def process(self, ctx: RenderContext) -> RenderContext:
        spec = ctx.spec
        bpm = _BPM_BY_MOOD[spec.mood]
        match = _BPM_PAT.search(spec.prompt)
        if match:
            bpm = max(40, min(200, int(match.group(1))))

        ctx.plan.update(
            bpm=bpm,
            key=_KEY_BY_MOOD[spec.mood],
            normalized_prompt=" ".join(spec.prompt.lower().split()),
            loop=spec.loop,
        )
        return ctx