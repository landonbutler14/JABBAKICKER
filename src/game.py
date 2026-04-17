import pygame
import sys
from src.audio_manager import AudioManager
from src.jabba import Jabba
from src.player import Player
from src.button import SimpleButton
from src.boot import Boot
from src.hud import HUD
from src.settings_panel import SettingsPanel, SettingsSlider
BLACK = (0, 0, 0)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FPS = 30

class Game:
    def __init__(self):
        pygame.init()
        
        """Assets to be loaded"""
        #Window and Clock================================
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        #Audio=========================
        self.audio = AudioManager()
        
        #Player==========================
        self.player = Player()
        
        #Boot============================
        self.boot = Boot("assets/images/boots/boot_basic.png")
        pygame.mouse.set_visible(True)

        #Background=====================
        self.jabbas_palace = pygame.image.load("assets/images/jabbas_palace.jpg").convert()      
        self.jabbas_palace = pygame.transform.scale(self.jabbas_palace, (WINDOW_WIDTH, WINDOW_HEIGHT)) 
        #Settings======================
        self.settings = SettingsPanel(self.window, self.audio)
        #Jabba============================
        self.jabba = Jabba(self.window)
        #Jabba Rectangle==================
        self.jabba_rect = pygame.Rect(600, 275, 480, 350)
        #Hud
        self.hud = HUD(self.window)
        #Upgrade Button====================
        
        #start the music=================
        self.audio.play_music("cantina_band.mp3")
        #============================
        self.running = True

    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.jabba.get_kicked(event.pos, self.player, self.audio, self.boot)
            self.settings.handle_event(event)


    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over Jabba
        hovering_jabba = self.jabba_rect.collidepoint(mouse_pos)

        # Update boot
        self.boot.update(mouse_pos, hovering_jabba)

        # Hide or show cursor
        pygame.mouse.set_visible(not hovering_jabba)


    def draw(self):
        self.window.fill(BLACK)
        self.window.blit(self.jabbas_palace, (0, 0))
        self.jabba.draw()
        self.hud.draw(self.player)
        self.settings.draw()
        self.boot.draw(self.window)
        pygame.display.update()


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
    