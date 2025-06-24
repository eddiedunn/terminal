# Cross-Platform Userland Binary Management: Design & Discussion

## Goals
- Reproducibility: Pin tool versions and ship known-good binaries for each platform/arch.
- Userland/Rootless: Deploy only to user directories, never system-wide.
- Cross-Platform: Support macOS (Darwin) and Linux (and potentially Windows in the future).
- Automation: Minimize manual steps for acquiring, verifying, and updating binaries.
- Integrated Experience: Shell configs and binaries are always in sync.

## Patterns
- Direct download from upstream releases (preferred)
- CI/CD built artifacts
- Package manager extraction (fallback)
- Source builds (fallback)

## Implementation
- See `BINARY_MANAGEMENT.md` for the current data model and process.
- All logic and data now live in the `tool_installer` role.

