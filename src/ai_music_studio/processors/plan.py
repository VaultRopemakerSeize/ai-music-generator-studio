"""Plan stage: turn analysis into a concrete arrangement (sections + loop points)."""

from __future__ import annotations

from dataclasses import dataclass

from ai_music_studio.processors.base import RenderContext


@dataclass(frozen=True, slots=True)
class Section:
    name: str
    start_s: float
    end_s: float
    gain_db: float


def _sections_for(seconds: int) -> list[Section]:
    """Intro / body / outro with a 2s crossfade-friendly tail."""
    intro = min(6.0, seconds * 0.1)
    outro = min(6.0, seconds * 0.1)
    body = max(0.0, seconds - intro - outro)
    return [
        Section("intro", 0.0, intro, -3.0),
        Section("body", intro, intro + body, 0.0),
        Section("outro", intro + body, seconds, -3.0),
    ]


class PlanProcessor:
    name = "plan"

    def process(self, ctx: RenderContext) -> RenderContext:
        ctx.plan["sections"] = _sections_for(ctx.spec.seconds)
        ctx.plan["loop_frames"] = int(ctx.plan["bpm"] / 60.0 * ctx.spec.sample_rate)
        return ctx