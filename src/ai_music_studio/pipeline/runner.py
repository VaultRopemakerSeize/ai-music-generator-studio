"""Pipeline runner: wires stages in order, runs them, returns a RenderResult."""

from __future__ import annotations

import logging
import time

from ai_music_studio.bootstrap import Runtime
from ai_music_studio.models.job import JobSpec, RenderResult
from ai_music_studio.processors import (
    AnalyzeProcessor,
    MasterProcessor,
    PlanProcessor,
    RenderProcessor,
)
from ai_music_studio.processors.base import Processor, RenderContext
from ai_music_studio.services.generation_service import GenerationService

log = logging.getLogger(__name__)


class PipelineRunner:
    def __init__(self, runtime: Runtime) -> None:
        self._runtime = runtime
        self._service = GenerationService(registry=runtime.registry, device=runtime.device)
        self._stages: list[Processor] = [
            AnalyzeProcessor(),
            PlanProcessor(),
            RenderProcessor(self._service),
            MasterProcessor(),
        ]

    def run(self, spec: JobSpec) -> RenderResult:
        ctx = RenderContext(spec=spec, sample_rate=spec.sample_rate)
        t0 = time.perf_counter()
        for stage in self._stages:
            t1 = time.perf_counter()
            ctx = stage.process(ctx)
            log.debug("stage=%s dt=%.3fs", stage.name, time.perf_counter() - t1)
        if ctx.audio is None:
            raise RuntimeError("pipeline produced no audio")
        log.info("pipeline done in %.2fs", time.perf_counter() - t0)
        return RenderResult(samples=ctx.audio, sample_rate=ctx.sample_rate, spec=spec)