import pygame

class Boot:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (150,150))
        self.rect = self.image.get_rect()
        
        # Whether the boot should be drawn instead of the cursor
        self.active = False

    def update(self, mouse_pos, active):
        self.active = active
        if self.active:
            self.rect.center = mouse_pos

    def draw(self, window):
        if self.active:
            window.blit(self.image, self.rect)

