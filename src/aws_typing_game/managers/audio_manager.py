"""
Audio manager for AWS Service Typing Game
"""

import math
import os
import random
import time
from typing import Dict, List, Optional

import pygame


class SoundGenerator:
    """Generates simple sound effects using pygame"""

    @staticmethod
    def generate_beep(
        frequency: int, duration: float, sample_rate: int = 22050
    ) -> pygame.mixer.Sound:
        """Generate a simple beep sound"""
        try:
            import numpy as np

            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * math.sin(2 * math.pi * frequency * i / sample_rate)
                arr.append([int(wave), int(wave)])

            # Convert to numpy array for pygame
            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
            return sound
        except ImportError:
            # Fallback: create a minimal silent sound
            return pygame.mixer.Sound(buffer=b"\x00\x00" * 1000)

    @staticmethod
    def generate_click(duration: float = 0.1, sample_rate: int = 22050) -> pygame.mixer.Sound:
        """Generate a typing click sound"""
        try:
            import numpy as np

            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                # Create a short burst of noise that fades out
                amplitude = 1000 * (1 - i / frames) * random.uniform(0.8, 1.2)
                noise = random.randint(-int(amplitude), int(amplitude))
                arr.append([noise, noise])

            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
            return sound
        except ImportError:
            # Fallback: create a minimal silent sound
            return pygame.mixer.Sound(buffer=b"\x00\x00" * 500)

    @staticmethod
    def generate_success_chord(
        duration: float = 0.5, sample_rate: int = 22050
    ) -> pygame.mixer.Sound:
        """Generate a success chord sound"""
        try:
            import numpy as np

            frames = int(duration * sample_rate)
            arr = []

            # Major chord frequencies (C4, E4, G4)
            frequencies = [261.63, 329.63, 392.00]

            for i in range(frames):
                wave = 0
                envelope = 1 - (i / frames)  # Fade out
                for freq in frequencies:
                    wave += envelope * 1000 * math.sin(2 * math.pi * freq * i / sample_rate)
                arr.append([int(wave), int(wave)])

            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
            return sound
        except ImportError:
            # Fallback: create a minimal silent sound
            return pygame.mixer.Sound(buffer=b"\x00\x00" * 1000)

    @staticmethod
    def generate_error_buzz(duration: float = 0.3, sample_rate: int = 22050) -> pygame.mixer.Sound:
        """Generate an error buzz sound"""
        try:
            import numpy as np

            frames = int(duration * sample_rate)
            arr = []

            for i in range(frames):
                # Low frequency buzz with some randomness
                envelope = 1 - (i / frames)
                wave = envelope * 2000 * math.sin(2 * math.pi * 100 * i / sample_rate)
                wave += envelope * 1000 * random.uniform(-0.3, 0.3)
                arr.append([int(wave), int(wave)])

            sound_array = np.array(arr, dtype=np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
            return sound
        except ImportError:
            # Fallback: create a minimal silent sound
            return pygame.mixer.Sound(buffer=b"\x00\x00" * 800)


class AudioManager:
    """Manages all audio functionality for the game"""

    def __init__(self):
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.audio_enabled = True
        except pygame.error:
            print("Warning: Audio could not be initialized")
            self.audio_enabled = False
            return

        # Audio settings
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.3  # Lower volume for relaxing BGM
        self.sfx_enabled = False  # Default OFF
        self.music_enabled = False  # Default OFF

        # Sound effects
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_tracks: List[str] = []
        self.current_music = None

        # Generate basic sound effects
        self._generate_default_sounds()

        # Audio folders
        self.sounds_folder = "assets/sounds"
        self.music_folder = "assets/music"

        # Create audio folders
        self.create_audio_folders()

        # Load custom sounds if available
        self._load_custom_sounds()

        # Typing sound timing
        self.last_type_sound = 0
        self.type_sound_interval = 0.05  # Minimum interval between typing sounds

    def _generate_default_sounds(self):
        """Generate default sound effects"""
        if not self.audio_enabled:
            return

        try:
            # Generate basic sound effects
            self.sounds["typing"] = SoundGenerator.generate_click(0.05)
            self.sounds["success"] = SoundGenerator.generate_success_chord(0.4)
            self.sounds["error"] = SoundGenerator.generate_error_buzz(0.2)
            self.sounds["menu_select"] = SoundGenerator.generate_beep(800, 0.1)
            self.sounds["menu_navigate"] = SoundGenerator.generate_beep(600, 0.05)
            self.sounds["game_start"] = SoundGenerator.generate_beep(1000, 0.3)
            self.sounds["game_over"] = SoundGenerator.generate_beep(300, 0.8)
            self.sounds["new_word"] = SoundGenerator.generate_beep(700, 0.1)

            # Set volumes for generated sounds
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume * self.master_volume)

        except Exception as e:
            print(f"Warning: Could not generate default sounds: {e}")

    def _load_custom_sounds(self):
        """Load custom sound files if available"""
        if not self.audio_enabled:
            return

        sound_files = {
            "typing": ["type.wav", "click.wav", "key.wav"],
            "success": ["success.wav", "correct.wav", "win.wav"],
            "error": ["error.wav", "wrong.wav", "buzz.wav"],
            "menu_select": ["select.wav", "confirm.wav"],
            "menu_navigate": ["navigate.wav", "move.wav"],
            "game_start": ["start.wav", "begin.wav"],
            "game_over": ["gameover.wav", "end.wav"],
            "new_word": ["newword.wav", "next.wav"],
        }

        if os.path.exists(self.sounds_folder):
            for sound_name, possible_files in sound_files.items():
                for filename in possible_files:
                    filepath = os.path.join(self.sounds_folder, filename)
                    if os.path.exists(filepath):
                        try:
                            self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                            self.sounds[sound_name].set_volume(self.sfx_volume * self.master_volume)
                            break
                        except pygame.error:
                            continue

        # Load music files
        if os.path.exists(self.music_folder):
            music_extensions = [".mp3", ".wav", ".ogg"]
            for filename in os.listdir(self.music_folder):
                if any(filename.lower().endswith(ext) for ext in music_extensions):
                    self.music_tracks.append(os.path.join(self.music_folder, filename))

        # Log music tracks status
        if self.music_tracks:
            print(f"Found {len(self.music_tracks)} music track(s)")
        else:
            print("No music files found in assets/music/ folder")

    def play_sound(self, sound_name: str, volume_override: Optional[float] = None):
        """Play a sound effect"""
        if not self.audio_enabled or not self.sfx_enabled:
            return

        if sound_name in self.sounds:
            sound = self.sounds[sound_name]

            # Special handling for typing sounds to prevent overlap
            if sound_name == "typing":
                current_time = time.time()
                if current_time - self.last_type_sound < self.type_sound_interval:
                    return
                self.last_type_sound = current_time

            if volume_override is not None:
                sound.set_volume(volume_override * self.master_volume)
            else:
                sound.set_volume(self.sfx_volume * self.master_volume)

            sound.play()

    def play_typing_sound(self):
        """Play typing sound with rate limiting"""
        self.play_sound("typing", 0.3)

    def play_success_sound(self):
        """Play success sound"""
        self.play_sound("success")

    def play_error_sound(self):
        """Play error sound"""
        self.play_sound("error")

    def play_menu_sound(self, action: str = "select"):
        """Play menu-related sound"""
        if action == "navigate":
            self.play_sound("menu_navigate", 0.5)
        else:
            self.play_sound("menu_select")

    def play_game_start_sound(self):
        """Play game start sound"""
        self.play_sound("game_start")

    def play_game_over_sound(self):
        """Play game over sound"""
        self.play_sound("game_over")

    def play_new_word_sound(self):
        """Play new word sound"""
        self.play_sound("new_word", 0.6)

    def start_background_music(self, track_name: Optional[str] = None):
        """Start playing background music"""
        if not self.audio_enabled or not self.music_enabled:
            return

        # Check if music tracks are available
        if not self.music_tracks:
            return  # No music to play

        try:
            if track_name:
                # Play specific track
                track_path = None
                for track in self.music_tracks:
                    if track_name in track:
                        track_path = track
                        break
                if not track_path:
                    return
            else:
                # Play random track
                track_path = random.choice(self.music_tracks)

            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.current_music = track_path
            print(f"Started playing BGM: {os.path.basename(track_path)}")

        except pygame.error as e:
            print(f"Warning: Could not play music: {e}")

    def stop_background_music(self):
        """Stop background music"""
        if self.audio_enabled:
            pygame.mixer.music.stop()
            self.current_music = None

    def pause_background_music(self):
        """Pause background music"""
        if self.audio_enabled:
            pygame.mixer.music.pause()

    def resume_background_music(self):
        """Resume background music"""
        if self.audio_enabled:
            pygame.mixer.music.unpause()

    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()

    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_sound_volumes()

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.audio_enabled:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def toggle_sfx(self):
        """Toggle sound effects on/off"""
        self.sfx_enabled = not self.sfx_enabled

    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_background_music()
        elif self.music_tracks:
            self.start_background_music()

    def _update_all_volumes(self):
        """Update all audio volumes"""
        self._update_sound_volumes()
        if self.audio_enabled:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def _update_sound_volumes(self):
        """Update sound effect volumes"""
        if not self.audio_enabled:
            return

        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)

    def create_audio_folders(self):
        """Create audio folders if they don't exist"""
        os.makedirs(self.sounds_folder, exist_ok=True)
        os.makedirs(self.music_folder, exist_ok=True)

        # Create readme files
        sounds_readme = os.path.join(self.sounds_folder, "README.txt")
        if not os.path.exists(sounds_readme):
            with open(sounds_readme, "w", encoding="utf-8") as f:
                f.write("""Sound Effects Folder

Place custom sound files here to replace the default generated sounds:

- typing.wav    : Typing sound
- success.wav   : Correct answer sound
- error.wav     : Wrong answer sound
- select.wav    : Menu selection sound
- navigate.wav  : Menu navigation sound
- start.wav     : Game start sound
- gameover.wav  : Game over sound
- newword.wav   : New word sound

Supported formats: WAV, OGG
""")

        music_readme = os.path.join(self.music_folder, "README.txt")
        if not os.path.exists(music_readme):
            with open(music_readme, "w", encoding="utf-8") as f:
                f.write("""Background Music Folder

Place background music files here for relaxing typing experience:

Supported formats: WAV, OGG, MP3

Recommended:
- Ambient/relaxing music
- Low volume instrumental tracks
- Loop-friendly compositions (30-60 seconds)
- No sudden volume changes

The game will randomly select from available tracks and loop them.
If no music files are present, the game runs silently.

Example filenames:
- relaxing_ambient.wav
- gentle_piano.ogg
- typing_focus.mp3
""")

    def get_audio_status(self) -> Dict[str, any]:
        """Get current audio status"""
        return {
            "audio_enabled": self.audio_enabled,
            "master_volume": self.master_volume,
            "sfx_volume": self.sfx_volume,
            "music_volume": self.music_volume,
            "sfx_enabled": self.sfx_enabled,
            "music_enabled": self.music_enabled,
            "current_music": os.path.basename(self.current_music) if self.current_music else None,
            "available_tracks": len(self.music_tracks),
            "loaded_sounds": list(self.sounds.keys()),
        }
