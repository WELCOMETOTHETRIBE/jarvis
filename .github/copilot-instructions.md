# Jarvis CLI — Copilot Instructions

This repository is a local‑first AI operator console built with Python.  Agents need to get up to speed quickly by understanding the high‑level architecture, coding conventions and developer workflows that are specific to this project.

---
## 🏗️ Architecture at a glance

- **Entry points**
  - `app/main.py` is the CLI powered by [Typer](https://typer.tiangolo.com/).  Commands are defined here and import their implementation lazily to keep startup fast.
  - `web/app.py` is a Streamlit UI mirroring many CLI commands.  It inserts `app/` onto `sys.path` so the same modules can be reused.

- **Core layers**
  - `app/core` contains shared utilities:
    - `config.py` loads environment variables (`.env`) and persists a small JSON config under `data/config.json`.
    - `paths.py` centralizes filesystem paths (`data/`, `workspaces/`, etc.) and ensures directories exist.
    - `models.py` defines Pydantic models used throughout (e.g., `WorkspaceConfig`, `Session`, `Message`).

- **Domain areas**
  - `app/cli` – user‑visible commands (chat, kb, workspace, media, doctor, etc.).
  - `app/llm` – language model providers (currently only `OpenAIProvider`).
  - `app/media` – image generation, TTS, STT, playback and vendor‑specific helpers.
  - `app/workspaces` – workspace CRUD and configuration.
  - `app/kb` – knowledge base search (stubbed for now).
  - `app/sessions` – session management (mostly TODOs that target a SQLite DB later).
  - `app/tools` – placeholder for tool integrations; currently empty.

- **Data & storage**
  - Local data lives under `data/` (sessions, audio, images, knowledge base, etc.).
  - `workspaces/` at the project root contains YAML configs and optional `system.md` prompts.
  - A SQLite file path is configured via `Config.db_path` but the database layer isn’t implemented yet.

- **Providers & external APIs**
  - OpenAI is the default LLM/image/voice/STT provider. Classes use `httpx` for HTTP calls.
  - Replicate and ElevenLabs are supported in several media modules.  API keys are read from environment variables (see `.env.example`).

---
## 🛠️ Developer workflows

1. **Setup**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   cp .env.example .env            # fill with keys
   python test_api_key.py          # quick sanity check
   jarvis doctor                   # more diagnostics
   ```

2. **Running**
   - CLI: `jarvis <command>`.  `jarvis help` shows available commands; each command has its own help.
   - Web UI: `jarvis web` or `streamlit run web/app.py`.
   - Tests: `pytest` (there are a few smoke tests under `tests/`).

3. **Adding a command**
   - Declare it in `app/main.py` with `@app.command()` and a helper function in `app/cli`.
   - Follow existing patterns (lazy import, Rich for console output, `Config/Paths` instantiation).
   - Update docs in README if user‑visible.

4. **Extending providers or media**
   - Create a new class under `app/llm` or `app/media`.
   - Constructor always receives a `Config` and `Paths` object; use them for keys and file storage.
   - Raise `ValueError` when required API keys are missing; follow existing error messages.
   - Add CLI flags to choose the provider if necessary (see `image` command for Replicate vs OpenAI logic).

5. **Workspace mechanics**
   - `WorkspaceConfig` (Pydantic) defines the structure stored in `workspaces/<slug>/workspace.yaml`.
   - `WorkspaceManager` in `app/workspaces/manager.py` handles listing, reading and creating workspaces.  System prompts are read from `system.md` if present.
   - Commands (e.g. `jarvis workspace list`/`use`) call the manager; the active workspace tracking is TODO but use `Config.default_workspace` as a hint.

6. **Knowledge base & sessions**
   - Both modules are currently stubs with `TODO` comments.  Implementations should interact with a database or a simple file store; tests will need to be added accordingly.
   - Use `Paths.kb` for KB storage and `Paths.sessions` for session data.

---
## 📦 Conventions & patterns

- **Configuration**: all runtime configuration lives in environment variables, with `.env` support via `python-dotenv`.  `Config` normalizes paths to absolute and lazy‑loads user prefs from `data/config.json`.
- **Filesystem paths**: use the `Paths` class everywhere instead of hard‑coding directories.
- **HTTP client**: `httpx.Client` is wrapped in provider classes with a 60‑second timeout.
- **Error handling**: raise Python exceptions (`ValueError`, `FileNotFoundError`) and let the CLI layer catch and display them in red text.  No custom exception classes yet.
- **Message formats**: LLM prompts are passed as `messages` arrays per OpenAI spec.  Other providers follow their respective API shapes.
- **Tests**: minimal right now; rely on `pytest` and simple asserts.  Add new tests for any new logic under `tests/`.

---
## 🧩 Integration points

- `app/main.py` uses `typer` and exposes subcommands; developers should look here first when adding functionality.
- `web/app.py` imports many of the same modules; changes to core business logic typically propagate immediately to the web UI.
- `app/core/paths.py` and `app/core/config.py` are the most‑imported modules; they are safe places to add shared helpers.
- The `.env.example` file lists all environment variables that the system reads (`OPENAI_API_KEY`, `REPLICATE_API_KEY`, `ELEVENLABS_API_KEY`, etc.).

---
## ✅ Tips for AI coding agents

- Keep responses short and pointed: the codebase is small and many pieces are stubs.
- When you encounter a `TODO` comment, inspect surrounding logic to mimic existing patterns.
- Use existing Pydantic models when adding new data structures.
- Refer to README for example CLI invocations; update it when adding new user‑facing features.
- Pay attention to places where `Paths` is used to create directories; new features that write files should follow the same idiom to avoid race conditions.

---
*Feel free to suggest clarifications or note missing pieces — I'll iterate on this guidance.*
