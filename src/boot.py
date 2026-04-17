import pygame
import math

class Boot:
    # Animation phases
    PHASE_IDLE = 'idle'
    PHASE_LUNGE = 'lunge'    # snapping forward
    PHASE_RECOIL = 'recoil'  # bouncing back

    # Tuning
    LUNGE_FRAMES = 3       # frames to snap forward
    RECOIL_FRAMES = 7      # frames to bounce back (slightly slower feels punchy)
    LUNGE_DISTANCE = 28    # pixels forward toward Jabba
    LUNGE_ROTATION = -25   # degrees — toe dips down on impact

    def __init__(self, image_path):
        self.base_image = pygame.image.load(image_path).convert_alpha()
        self.base_image = pygame.transform.smoothscale(self.base_image, (150, 150))

        self.image = self.base_image
        self.rect = self.image.get_rect()

        self.active = False

        # Animation state
        self.phase = Boot.PHASE_IDLE
        self.frame = 0

        # Positions
        self.mouse_pos = (0, 0)   # where the cursor actually is
        self.draw_pos = (0, 0)    # where we render the boot (may be offset)

    def trigger_kick(self):
        """Call this when a kick lands to start the animation."""
        self.phase = Boot.PHASE_LUNGE
        self.frame = 0

    def _ease_out(self, t):
        """Quadratic ease-out: fast start, slow finish."""
        return 1 - (1 - t) ** 2

    def _ease_in(self, t):
        """Quadratic ease-in: slow start, fast finish."""
        return t ** 2

    def update(self, mouse_pos, active):
        self.active = active
        self.mouse_pos = mouse_pos

        if not self.active:
            self.phase = Boot.PHASE_IDLE
            self.frame = 0

        offset_x = 0
        offset_y = 0
        rotation = 0

        if self.phase == Boot.PHASE_LUNGE:
            t = self._ease_out(self.frame / Boot.LUNGE_FRAMES)
            offset_x = int(Boot.LUNGE_DISTANCE * t)
            rotation = Boot.LUNGE_ROTATION * t
            self.frame += 1
            if self.frame > Boot.LUNGE_FRAMES:
                self.phase = Boot.PHASE_RECOIL
                self.frame = 0

        elif self.phase == Boot.PHASE_RECOIL:
            t = self._ease_in(self.frame / Boot.RECOIL_FRAMES)
            offset_x = int(Boot.LUNGE_DISTANCE * (1 - t))
            rotation = Boot.LUNGE_ROTATION * (1 - t)
            self.frame += 1
            if self.frame > Boot.RECOIL_FRAMES:
                self.phase = Boot.PHASE_IDLE
                self.frame = 0

        # Apply rotation if mid-animation
        if rotation != 0:
            self.image = pygame.transform.rotate(self.base_image, rotation)
        else:
            self.image = self.base_image

        # Offset is rightward (toward Jabba on the right side)
        cx = mouse_pos[0] + offset_x
        cy = mouse_pos[1] + offset_y
        self.rect = self.image.get_rect(center=(cx, cy))

    def draw(self, window):
        if self.active:
            window.blit(self.image, self.rect)