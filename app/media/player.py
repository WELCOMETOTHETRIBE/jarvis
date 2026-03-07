"""Media playback utilities"""

import subprocess
import sys
from pathlib import Path
from typing import Optional
from app.core.config import Config
from app.core.paths import Paths

class MediaPlayer:
    """Play audio and video files"""

    def __init__(self, config: Config, paths: Paths):
        self.config = config
        self.paths = paths

    def play_audio(self, audio_path: Path, blocking: bool = True) -> None:
        """Play an audio file"""

        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if sys.platform == "darwin":  # macOS
            cmd = ["afplay", str(audio_path)]
        elif sys.platform == "linux":
            cmd = ["aplay", str(audio_path)]
        elif sys.platform == "win32":
            cmd = ["start", str(audio_path)]
        else:
            raise NotImplementedError(f"Audio playback not supported on {sys.platform}")

        if blocking:
            subprocess.run(cmd, check=True)
        else:
            subprocess.Popen(cmd)

    def play_video(self, video_path: Path, blocking: bool = True) -> None:
        """Play a video file"""

        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        if sys.platform == "darwin":  # macOS
            cmd = ["open", str(video_path)]
        elif sys.platform == "linux":
            cmd = ["xdg-open", str(video_path)]
        elif sys.platform == "win32":
            cmd = ["start", str(video_path)]
        else:
            raise NotImplementedError(f"Video playback not supported on {sys.platform}")

        if blocking:
            subprocess.run(cmd, check=True)
        else:
            subprocess.Popen(cmd)