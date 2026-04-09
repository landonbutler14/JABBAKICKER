import pygame
import sys
from src.audio_manager import AudioManager
from src.jabba import Jabba
from src.player import Player
from src.button import SimpleButton

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

        #Background=====================
        self.jabbas_palace = pygame.image.load("assets/images/jabbas_palace.jpg").convert()      
        self.jabbas_palace = pygame.transform.scale(self.jabbas_palace, (WINDOW_WIDTH, WINDOW_HEIGHT))  
        #Jabba============================
        self.jabba = Jabba(self.window)
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
                self.jabba.get_kicked(event.pos, self.player, self.audio)
                

    def update(self):
        pass  # game logic goes here

    def draw(self):
        self.window.fill(BLACK)
        self.window.blit(self.jabbas_palace, (0, 0))
        self.jabba.draw()
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
    