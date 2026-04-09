import pygame

class Jabba():
    def __init__(self, window):
        self.jabba_image = pygame.image.load("assets/images/jabba.png").convert_alpha()
        self.jabba_image = pygame.transform.smoothscale(self.jabba_image, (480, 350))

        self.window = window
        self.x = 600
        self.y = 275
        self.rect = pygame.Rect(self.x, self.y, 480, 350)

    
    def draw(self):
        self.window.blit(self.jabba_image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    def get_kicked(self, mouse_pos, player, audio):
        if self.rect.collidepoint(mouse_pos):
            earned = player.kick()
            player.credits += earned
            audio.play_sfx("kick.mp3")
            print(f"+{earned} credits! Total: {player.credits}")
            return True

        return False
    
    