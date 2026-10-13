"""Pipeline processors. Each stage: `process(ctx) -> ctx`."""

from ai_music_studio.processors.base import Processor, RenderContext
from ai_music_studio.processors.analyze import AnalyzeProcessor
from ai_music_studio.processors.plan import PlanProcessor
from ai_music_studio.processors.render import RenderProcessor
from ai_music_studio.processors.master import MasterProcessor

__all__ = [
    "Processor",
    "RenderContext",
    "AnalyzeProcessor",
    "PlanProcessor",
    "RenderProcessor",
    "MasterProcessor",
]