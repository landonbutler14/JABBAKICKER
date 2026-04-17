import pygame
from pathlib import Path

class AudioManager:
    def __init__(self, base_path="assets/sounds"):
        pygame.mixer.init()

        self.base_path = Path(base_path)

        # Volume settings (0.0 to 1.0)
        self.master_volume = 1.0
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # Cache for loaded sound effects
        self.sfx_cache = {}

    def _effective_music_volume(self):
        return self.master_volume * self.music_volume

    def _effective_sfx_volume(self):
        return self.master_volume * self.sfx_volume

    def play_music(self, filename, loop=-1):
        path = self.base_path / filename
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self._effective_music_volume())
        pygame.mixer.music.play(loop)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_master_volume(self, value):
        self.master_volume = max(0.0, min(1.0, value))
        pygame.mixer.music.set_volume(self._effective_music_volume())

    def set_music_volume(self, value):
        self.music_volume = max(0.0, min(1.0, value))
        pygame.mixer.music.set_volume(self._effective_music_volume())

    def load_sfx(self, filename):
        if filename not in self.sfx_cache:
            path = self.base_path / filename
            self.sfx_cache[filename] = pygame.mixer.Sound(path)
        return self.sfx_cache[filename]

    def play_sfx(self, filename):
        sound = self.load_sfx(filename)
        sound.set_volume(self._effective_sfx_volume())
        sound.play()

    def set_sfx_volume(self, value):
        self.sfx_volume = max(0.0, min(1.0, value))