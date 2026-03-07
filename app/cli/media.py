"""Media generation commands"""

import typer
from pathlib import Path
from enum import Enum
from rich.console import Console
from rich.progress import Progress
from app.core.config import Config
from app.core.paths import Paths
from app.media.image_gen import ImageGenerator
from app.media.tts import TextToSpeech
from app.media.elevenlabs_tts import ElevenLabsTTS
from app.media.stt import SpeechToText
from app.media.player import MediaPlayer


class ImageModel(str, Enum):
    """Allowed image generation providers/models."""

    DALLE = "dall-e-3"
    REPLICATE = "replicate"

app = typer.Typer()
console = Console()

# ElevenLabs free voices
ELEVENLABS_VOICES = ["Sarah", "Laura", "Charlie", "George", "River", "Alice", "Matilda", "Jessica", "Bella"]
OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

def get_tts_provider(voice: str):
    """Determine which TTS provider to use based on voice name"""
    if voice in ELEVENLABS_VOICES:
        return "elevenlabs"
    elif voice in OPENAI_VOICES:
        return "openai"
    else:
        return "openai"  # Default to OpenAI

@app.command()
def image(
    prompt: str = typer.Argument(..., help="Image description prompt"),
    model: ImageModel = typer.Option(
        ImageModel.DALLE,
        help="Image provider/model to use",
    ),
    size: str = typer.Option("1024x1024", help="Image size"),
    quality: str = typer.Option("standard", help="Image quality"),
    output: Path = typer.Option(None, help="Output file path")
):
    """Generate an image from text prompt (choices are dall-e-3 or replicate)"""
    config = Config()
    paths = Paths(config)
    generator = ImageGenerator(config, paths)

    with Progress() as progress:
        task = progress.add_task("Generating image...", total=100)

        try:
            progress.update(task, advance=50)
            image_path = generator.generate_image(
                prompt=prompt,
                model=model,
                size=size,
                quality=quality,
                output_path=output
            )
            progress.update(task, advance=50)

            console.print(f"✅ Image generated: [link=file://{image_path}]{image_path}[/link]")
            console.print(f"📂 Saved to: {image_path}")

        except Exception as e:
            console.print(f"❌ Error generating image: {e}", style="red")

@app.command()
def tts(
    text: str = typer.Argument(..., help="Text to convert to speech"),
    voice: str = typer.Option("nova", help="Voice to use"),
    model: str = typer.Option("tts-1", help="TTS model (OpenAI only)"),
    output: Path = typer.Option(None, help="Output file path"),
    play: bool = typer.Option(False, help="Play the audio after generation")
):
    """Convert text to speech"""
    config = Config()
    paths = Paths(config)
    player = MediaPlayer(config, paths) if play else None

    # Determine provider based on voice
    provider = get_tts_provider(voice)
    
    with Progress() as progress:
        task = progress.add_task("Generating speech...", total=100)

        try:
            progress.update(task, advance=50)
            
            if provider == "elevenlabs":
                tts_engine = ElevenLabsTTS(config, paths)
                audio_path = tts_engine.generate_speech(
                    text=text,
                    voice=voice,
                    output_path=output
                )
            else:
                tts_engine = TextToSpeech(config, paths)
                audio_path = tts_engine.generate_speech(
                    text=text,
                    voice=voice,
                    model=model,
                    output_path=output
                )
            
            progress.update(task, advance=50)

            console.print(f"✅ Speech generated: [link=file://{audio_path}]{audio_path}[/link]")
            console.print(f"📂 Saved to: {audio_path}")
            console.print(f"🎤 Provider: {provider.upper()}")

            if play:
                console.print("🔊 Playing audio...")
                player.play_audio(audio_path)

        except Exception as e:
            console.print(f"❌ Error generating speech: {e}", style="red")

@app.command()
def stt(
    audio_file: Path = typer.Argument(..., help="Audio file to transcribe"),
    language: str = typer.Option(None, help="Language code (e.g., 'en', 'es')"),
    translate: bool = typer.Option(False, help="Translate to English"),
    model: str = typer.Option("whisper-1", help="STT model")
):
    """Convert speech to text"""
    config = Config()
    paths = Paths(config)
    stt_engine = SpeechToText(config, paths)

    if not audio_file.exists():
        console.print(f"❌ Audio file not found: {audio_file}", style="red")
        return

    with Progress() as progress:
        task = progress.add_task("Transcribing audio...", total=100)

        try:
            progress.update(task, advance=50)

            if translate:
                text = stt_engine.translate_audio(audio_file, model=model)
                console.print("🌍 Translated text:")
            else:
                text = stt_engine.transcribe_audio(
                    audio_file,
                    model=model,
                    language=language
                )
                console.print("📝 Transcribed text:")

            progress.update(task, advance=50)
            console.print(f"\n{text}\n")

        except Exception as e:
            console.print(f"❌ Error transcribing audio: {e}", style="red")

@app.command()
def voices():
    """List available TTS voices"""
    config = Config()
    paths = Paths(config)
    tts_engine = TextToSpeech(config, paths)

    voices_dict = tts_engine.list_voices()
    
    console.print("\n🎤 [bold]Available TTS Voices[/bold]\n")
    
    # OpenAI voices
    console.print("[cyan]OpenAI TTS:[/cyan]")
    for voice in voices_dict.get("openai", []):
        marker = "⭐" if voice == config.default_voice else "  "
        console.print(f"  {marker} {voice}")
    
    # ElevenLabs free voices
    console.print("\n[cyan]ElevenLabs Free Tier:[/cyan]")
    for voice in voices_dict.get("elevenlabs_free", []):
        marker = "⭐" if voice == config.default_voice else "  "
        console.print(f"  {marker} {voice}")
    
    console.print(f"\n[green]Current default: {config.default_voice}[/green]")
    console.print("[yellow]Use 'jarvis voice <name>' to set default[/yellow]\n")

@app.command()
def set_voice(
    name: str = typer.Argument(..., help="Voice name to set as default")
):
    """Set default TTS voice"""
    config = Config()
    paths = Paths(config)
    tts_engine = TextToSpeech(config, paths)
    
    voices_dict = tts_engine.list_voices()
    all_voices = voices_dict.get("openai", []) + voices_dict.get("elevenlabs_free", [])
    
    if name not in all_voices:
        console.print(f"❌ Voice '{name}' not found", style="red")
        console.print(f"Available voices: {', '.join(all_voices)}", style="yellow")
        return
    
    # Update config file - save to a config.json
    import json
    config_file = paths.data / "config.json"
    
    try:
        if config_file.exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
        else:
            user_config = {}
        
        user_config["default_voice"] = name
        
        with open(config_file, 'w') as f:
            json.dump(user_config, f, indent=2)
        
        console.print(f"✅ Default voice set to: [bold green]{name}[/bold green]")
    except Exception as e:
        console.print(f"❌ Error saving voice preference: {e}", style="red")

@app.command()
def play(
    media_file: Path = typer.Argument(..., help="Media file to play"),
    blocking: bool = typer.Option(True, help="Wait for playback to finish")
):
    """Play audio or video files"""
    config = Config()
    paths = Paths(config)
    player = MediaPlayer(config, paths)

    if not media_file.exists():
        console.print(f"❌ Media file not found: {media_file}", style="red")
        return

    try:
        if media_file.suffix.lower() in ['.mp3', '.wav', '.m4a', '.aac']:
            console.print(f"🔊 Playing audio: {media_file}")
            player.play_audio(media_file, blocking=blocking)
        elif media_file.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
            console.print(f"🎬 Playing video: {media_file}")
            player.play_video(media_file, blocking=blocking)
        else:
            console.print(f"❌ Unsupported media format: {media_file.suffix}", style="red")

    except Exception as e:
        console.print(f"❌ Error playing media: {e}", style="red")