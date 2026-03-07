# Jarvis CLI

A local-first AI operator console with retrieval, tools, media, and workspace-aware context.

## Features

- **Local-first architecture**: Works offline with local knowledge bases
- **Workspace-aware**: Different contexts for different domains
- **Knowledge base**: Ingest and search documents
- **Tool execution**: Safe tool integration
- **Multi-modal**: Text, images, voice (planned)
- **Web UI**: Intuitive web interface alongside CLI

## ✅ **Status: Fully Functional!**

All core features are now working:
- ✅ CLI chat and commands
- ✅ Workspace management
- ✅ Knowledge base search
- ✅ **Image generation** (DALL-E 3)
- ✅ **Text-to-speech** (OpenAI TTS)
- ✅ **Speech-to-text** (Whisper)
- ✅ Web UI with media controls
- ✅ Local file storage

## Quick Start

1. **Install dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Test your API key**:
   ```bash
   python test_api_key.py
   ```

   If the test fails, make sure you have a valid OpenAI API key from https://platform.openai.com/api-keys

3. **Run diagnostics**:
   ```bash
   jarvis doctor
   ```

4. **Launch the web UI**:
   ```bash
   jarvis web
   ```
   Or directly:
   ```bash
   streamlit run web/app.py
   ```

   The web UI will be available at http://localhost:8501

5. **Use the CLI**:
   ```bash
   jarvis doctor                    # Check system status
   jarvis chat                      # Interactive chat
   jarvis ask "What is AI?"         # Single question
   jarvis kb search "python"        # Search knowledge base
   jarvis workspace list            # List workspaces
   jarvis workspace use mactech     # Switch workspace

   # Media Generation Commands
   jarvis image "A sunset over mountains"  # Generate image
   jarvis tts "Hello world" --voice alloy --play  # Text to speech
   jarvis stt audio.wav                    # Speech to text
   jarvis voices                           # List TTS voices
   jarvis play generated_audio.mp3         # Play media files
   ```

## Workspaces

Jarvis supports multiple workspaces for different contexts:

- **general**: General purpose assistant
- **mactech**: Secure compliance and GovCon engineering
- **wttt**: [Coming soon]
- **jabronis**: [Coming soon]

Switch workspaces:
```bash
jarvis workspace use mactech
```

## Architecture

- **Backend**: Python with FastAPI/CLI
- **Frontend**: Streamlit web UI
- **Database**: SQLite for local development
- **Storage**: Filesystem for documents, images, etc.
- **Providers**: OpenAI (extensible to others)

## Media Generation Examples

### Image Generation
```bash
# Generate a high-quality image
jarvis image "A futuristic cityscape at night with flying cars"

# Generate with specific parameters
jarvis image "A serene mountain lake" --model dall-e-3 --size 1792x1024 --quality hd

# or use Replicate if you have a key/credits:
jarvis image "A serene mountain lake" --model replicate --size 1024x1024

# Save to specific location
jarvis image "Abstract art with blue and gold colors" --output my_art.png
```

### Text-to-Speech
```bash
# Basic TTS
jarvis tts "Hello, welcome to Jarvis AI!"

# With different voice and auto-play
jarvis tts "This is a test message" --voice nova --play

# Save to file
jarvis tts "Important announcement" --output announcement.mp3
```

### Speech-to-Text
```bash
# Transcribe an audio file
jarvis stt recording.wav

# Transcribe with language hint
jarvis stt spanish_audio.wav --language es

# Translate foreign speech to English
jarvis stt foreign_speech.wav --translate
```

### Media Playback
```bash
# Play generated audio
jarvis play tts_output.mp3

# Play in background (non-blocking)
jarvis play music.mp3 --blocking false
```

## Project Structure

```
jarvis-cli/
├── app/                 # Core application
│   ├── cli/            # CLI commands
│   ├── core/           # Configuration, models, utils
│   ├── llm/            # LLM providers
│   ├── kb/             # Knowledge base
│   ├── db/             # Database layer
│   ├── sessions/       # Session management
│   ├── workspaces/     # Workspace management
│   └── tools/          # Tool integrations
├── web/                # Web UI (Streamlit)
├── data/               # Local data storage
├── workspaces/         # Workspace configurations
└── docs/               # Documentation
```

## Security

- Local-first: Your data stays on your machine
- Tool safety: Destructive operations require confirmation
- Redaction: Sensitive information is automatically redacted
- Audit logs: All operations are logged for compliance

## Roadmap

- [ ] Advanced KB with embeddings
- [ ] Image generation and editing
- [ ] Text-to-speech and speech-to-text
- [ ] Enterprise security features
- [ ] Multi-user support
- [ ] Plugin system