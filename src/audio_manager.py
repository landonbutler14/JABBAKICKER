import pygame
from pathlib import Path

class AudioManager:
    def __init__(self, base_path="assets/sounds"):
        pygame.mixer.init()

        # Store paths
        self.base_path = Path(base_path)
        # Volume settings
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # Cache for loaded sound effects
        self.sfx_cache = {}

    def play_music(self, filename, loop=-1):
        """Load and play background music."""
        path = self.base_path / filename
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_music_volume(self, value):
        """Clamp volume between 0 and 1."""
        self.music_volume = max(0, min(1, value))
        pygame.mixer.music.set_volume(self.music_volume)

    # -----------------------------
    # Sound Effects
    # -----------------------------
    def load_sfx(self, filename):
        """Load a sound effect once and cache it."""
        if filename not in self.sfx_cache:
            path = self.base_path / filename
            self.sfx_cache[filename] = pygame.mixer.Sound(path)
        return self.sfx_cache[filename]

    def play_sfx(self, filename):
        """Play a cached sound effect."""
        sound = self.load_sfx(filename)
        sound.set_volume(self.sfx_volume)
        sound.play()

    def set_sfx_volume(self, value):
        self.sfx_volume = max(0, min(1, value))