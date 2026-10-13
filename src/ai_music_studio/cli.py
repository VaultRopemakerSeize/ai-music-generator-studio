"""Typer CLI entry point. `aims generate --mood calm --seconds 90 --out loop.wav`."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ai_music_studio.bootstrap import bootstrap
from ai_music_studio.handlers.prompt_handler import PromptHandler
from ai_music_studio.models.job import JobSpec, Mood
from ai_music_studio.pipeline.runner import PipelineRunner

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@app.command()
def generate(
    prompt: Annotated[str, typer.Option("--prompt", "-p")] = "warm ambient pad, slow",
    mood: Annotated[Mood, typer.Option("--mood", "-m")] = Mood.CALM,
    seconds: Annotated[int, typer.Option("--seconds", "-s", min=4, max=600)] = 60,
    out: Annotated[Path, typer.Option("--out", "-o")] = Path("outputs/track.wav"),
    seed: Annotated[int | None, typer.Option("--seed")] = None,
    force_cpu: Annotated[bool, typer.Option("--cpu")] = False,
) -> None:
    """Generate one loopable background track."""
    rt = bootstrap(force_cpu=force_cpu)
    spec = PromptHandler(registry=rt.registry).build_spec(
        prompt=prompt, mood=mood, seconds=seconds, seed=seed, device=rt.device
    )
    result = PipelineRunner(runtime=rt).run(spec)
    result.write(out)
    console.print(f"[green]ok[/green] {out}  {result.duration_s:.1f}s  {result.sample_rate}Hz")


@app.command()
def devices() -> None:
    """List audio output devices the export driver can target."""
    from ai_music_studio.drivers.file_driver import FileDriver

    for idx, name in FileDriver.enumerate_devices():
        console.print(f"{idx:>3}  {name}")


if __name__ == "__main__":
    app()