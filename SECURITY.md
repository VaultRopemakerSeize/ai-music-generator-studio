# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Open a private security advisory on GitHub, or email
`security@ai-music-generator-studio.invalid` (PGP key in `docs/pgp.txt`).
Do not open a public issue for memory-safety bugs in the native kernels —
those get a coordinated fix and a CVE if warranted.

## Threat model

This is an offline desktop tool. The realistic attack surface is:

1. **Model weight files** loaded from `models/weights/`. We treat `.safetensors`
   as safe; we treat `.pt`/`.ckpt`/`.bin` as untrusted and refuse to load them
   unless `--allow-unsafe-weights` is passed. Pickle deserialization is the
   classic RCE vector here.
2. **Preset files** (`models/presets/*.toml`). TOML only, no `eval`, no
   `exec`. A malicious preset can't do more than crash the renderer.
3. **Native sidecar DLLs**. Loaded via `ctypes` with `os.add_dll_directory`.
   We verify SHA-256 against `native/checksums.txt` before load.
4. **Export paths**. All writes go through `utils/paths.safe_join` to prevent
   `..\` traversal from a crafted project file.

## Out of scope

- Malicious audio content. We don't scan samples.
- DLL sideloading in the host process. That's the OS's problem.
- Anything requiring local admin. We never request elevation.