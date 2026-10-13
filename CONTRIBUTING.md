# Contributing to ai-music-generator-studio

Thanks for wanting to push the pipeline forward. This repo is a Windows-first
desktop tool that turns a prompt + mood + tempo into loopable background music
using local AI models (MusicGen-family, Stable Audio Open, and a small
procedural fallback engine). Everything runs offline by default.

## Ground rules

- **Python 3.11+** is the reference runtime. Type hints mandatory on all public
  functions. `mypy --strict` on `src/ai_music_studio/`.
- **Formatting**: `ruff format` + `ruff check`. Line length 100.
- **Tests**: `pytest -q`. New pipeline stages need at least one unit test and
  one golden-file integration test under `tests/fixtures/`.
- **Native sidecars** (`native/dsp_kernels/`, `native/audio_io/`) build via
  CMake and are optional — the pure-Python path must always work.

## Pipeline overview

```
ingest -> analyze -> plan -> render -> master -> export
```

Each stage is a `Processor` subclass. Handlers in `src/ai_music_studio/handlers/`
wire stages to file formats and CLI/GUI entry points. Drivers in
`src/ai_music_studio/drivers/` own the audio backends (WASAPI, ASIO, PortAudio,
file). Services in `src/ai_music_studio/services/` own the long-lived model
sessions.

## What we want PRs for

- New mood presets in `models/presets/`
- New export formats (Opus, tracker MOD, WAV stems)
- Faster DSP kernels (SIMD, AVX2, NEON-for-ARM64 Windows)
- Better loop-point detection
- Interop bindings: C# (NAudio host), Java (JFugue bridge)

## What we don't merge

- Anything that phones home. No telemetry, no cloud render, no API keys
  baked into presets.
- Model weights. Weights live in `models/weights/` and are pulled via
  `scripts/fetch_weights.py`. Never commit binaries.
- GPL-incompatible licenses in vendored code.

## Commit style

Conventional Commits. `feat(render): add groove-quantized loop points`.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,native,gui]"
python scripts/fetch_weights.py --family musicgen-small
pytest -q
```