import pygame

# Colors — matching HUD Star Wars palette
GOLD = (200, 160, 50)
GOLD_DIM = (140, 110, 35)
DARK_BG = (10, 8, 5)
PANEL_BORDER = (180, 140, 40)
TEXT_WHITE = (230, 220, 190)
SLIDER_TRACK = (60, 50, 30)
SLIDER_FILL = (200, 160, 50)
SLIDER_HANDLE = (230, 190, 80)
SLIDER_HANDLE_HOVER = (255, 220, 100)

ICON_SIZE = 48
ICON_X = 16
ICON_Y = 16

PANEL_X = 16
PANEL_Y = ICON_Y + ICON_SIZE + 8
PANEL_WIDTH = 280
PANEL_HEIGHT = 210
BORDER_RADIUS = 6
BORDER_THICKNESS = 2
PANEL_ALPHA = 210

SLIDER_TRACK_HEIGHT = 4
SLIDER_HANDLE_RADIUS = 8
SLIDER_LEFT = 16
SLIDER_RIGHT = PANEL_WIDTH - 16
SLIDER_USABLE = SLIDER_RIGHT - SLIDER_LEFT


class SettingsSlider:
    def __init__(self, label, value, y_offset):
        self.label = label
        self.value = value          # 0.0 to 1.0
        self.y_offset = y_offset    # y position inside the panel surface
        self.dragging = False
        self.hovering = False

    def get_handle_x(self):
        return int(SLIDER_LEFT + self.value * SLIDER_USABLE)

    def get_handle_rect_abs(self, panel_y):
        """Handle rect in window coordinates for hit testing."""
        hx = PANEL_X + self.get_handle_x()
        hy = panel_y + self.y_offset
        return pygame.Rect(hx - SLIDER_HANDLE_RADIUS, hy - SLIDER_HANDLE_RADIUS,
                           SLIDER_HANDLE_RADIUS * 2, SLIDER_HANDLE_RADIUS * 2)

    def get_track_rect_abs(self, panel_y):
        """Full track rect in window coordinates for click-to-seek."""
        hy = panel_y + self.y_offset
        return pygame.Rect(PANEL_X + SLIDER_LEFT, hy - 10,
                           SLIDER_USABLE, 20)

    def set_value_from_x(self, abs_x):
        rel_x = abs_x - PANEL_X - SLIDER_LEFT
        self.value = max(0.0, min(1.0, rel_x / SLIDER_USABLE))

    def draw(self, surface, font_small):
        # Label + percentage
        label_surf = font_small.render(self.label, True, GOLD_DIM)
        pct_surf = font_small.render(f"{int(self.value * 100)}%", True, TEXT_WHITE)
        surface.blit(label_surf, (SLIDER_LEFT, self.y_offset - 18))
        surface.blit(pct_surf, (PANEL_WIDTH - pct_surf.get_width() - SLIDER_LEFT,
                                self.y_offset - 18))

        # Track background
        pygame.draw.rect(surface, SLIDER_TRACK,
                         (SLIDER_LEFT, self.y_offset - SLIDER_TRACK_HEIGHT // 2,
                          SLIDER_USABLE, SLIDER_TRACK_HEIGHT),
                         border_radius=2)

        # Track fill
        fill_w = int(self.value * SLIDER_USABLE)
        if fill_w > 0:
            pygame.draw.rect(surface, SLIDER_FILL,
                             (SLIDER_LEFT, self.y_offset - SLIDER_TRACK_HEIGHT // 2,
                              fill_w, SLIDER_TRACK_HEIGHT),
                             border_radius=2)

        # Handle
        hx = self.get_handle_x()
        color = SLIDER_HANDLE_HOVER if (self.hovering or self.dragging) else SLIDER_HANDLE
        pygame.draw.circle(surface, color, (hx, self.y_offset), SLIDER_HANDLE_RADIUS)
        pygame.draw.circle(surface, PANEL_BORDER, (hx, self.y_offset),
                           SLIDER_HANDLE_RADIUS, 1)


class SettingsPanel:
    def __init__(self, window, audio):
        self.window = window
        self.audio = audio
        self.open = False

        # Icon
        raw_icon = pygame.image.load("assets/images/settings_icon.png").convert_alpha()
        self.icon = pygame.transform.smoothscale(raw_icon, (ICON_SIZE, ICON_SIZE))
        self.icon_rect = pygame.Rect(ICON_X, ICON_Y, ICON_SIZE, ICON_SIZE)

        # Load up da Font
        self.font_large = pygame.font.Font("assets/fonts/starjedi.ttf", 16)
        self.font_small = pygame.font.Font("assets/fonts/starjedi.ttf", 13)

        # Panel surface
        self.panel_surf = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT), pygame.SRCALPHA)

        # Sliders — y_offset is position within the panel surface
        self.sliders = [
            SettingsSlider("MASTER", audio.master_volume, 75),
            SettingsSlider("MUSIC",  audio.music_volume,  135),
            SettingsSlider("SFX",    audio.sfx_volume,    190),
        ]

    def _draw_panel_bg(self):
        self.panel_surf.fill((0, 0, 0, 0))
        bg_rect = pygame.Rect(0, 0, PANEL_WIDTH, PANEL_HEIGHT)
        pygame.draw.rect(self.panel_surf, (*DARK_BG, PANEL_ALPHA),
                         bg_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.panel_surf, (*PANEL_BORDER, 255),
                         bg_rect, width=BORDER_THICKNESS,
                         border_radius=BORDER_RADIUS)
        # Inner highlight
        pygame.draw.line(self.panel_surf, (*GOLD, 80),
                         (BORDER_RADIUS, BORDER_THICKNESS + 2),
                         (PANEL_WIDTH - BORDER_RADIUS, BORDER_THICKNESS + 2), 1)

    def handle_event(self, event):
        if not self.open:
            # Only care about icon clicks when closed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.icon_rect.collidepoint(event.pos):
                    self.open = True
            return

        # Close if clicking outside panel and icon
        panel_rect = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.icon_rect.collidepoint(event.pos):
                self.open = False
                return
            if not panel_rect.collidepoint(event.pos):
                self.open = False
                return
            # Check slider handle / track hits
            for slider in self.sliders:
                if slider.get_handle_rect_abs(PANEL_Y).collidepoint(event.pos):
                    slider.dragging = True
                elif slider.get_track_rect_abs(PANEL_Y).collidepoint(event.pos):
                    slider.set_value_from_x(event.pos[0])
                    self._apply_volumes()

        elif event.type == pygame.MOUSEBUTTONUP:
            for slider in self.sliders:
                slider.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            for slider in self.sliders:
                slider.hovering = slider.get_handle_rect_abs(PANEL_Y).collidepoint(mouse_pos)
                if slider.dragging:
                    slider.set_value_from_x(mouse_pos[0])
                    self._apply_volumes()

    def _apply_volumes(self):
        """Push slider values to AudioManager."""
        master = self.sliders[0].value
        music  = self.sliders[1].value
        sfx    = self.sliders[2].value
        self.audio.set_master_volume(master)
        self.audio.set_music_volume(music)
        self.audio.set_sfx_volume(sfx)

    def _draw_icon_box(self):
        """Draw a dark semi-transparent box behind the settings icon."""
        padding = 8
        box_surf = pygame.Surface(
            (ICON_SIZE + padding * 2, ICON_SIZE + padding * 2), pygame.SRCALPHA
        )
        box_rect = pygame.Rect(0, 0, ICON_SIZE + padding * 2, ICON_SIZE + padding * 2)

        # Dark fill
        pygame.draw.rect(box_surf, (*DARK_BG, PANEL_ALPHA),
                         box_rect, border_radius=BORDER_RADIUS)
        # Gold border
        pygame.draw.rect(box_surf, (*PANEL_BORDER, 255),
                         box_rect, width=BORDER_THICKNESS,
                         border_radius=BORDER_RADIUS)
        # Inner highlight
        pygame.draw.line(box_surf, (*GOLD, 80),
                         (BORDER_RADIUS, BORDER_THICKNESS + 2),
                         (ICON_SIZE + padding * 2 - BORDER_RADIUS, BORDER_THICKNESS + 2), 1)

        self.window.blit(box_surf, (ICON_X - padding, ICON_Y - padding))

    def draw(self):
        # Always draw icon box and icon
        self._draw_icon_box()
        self.window.blit(self.icon, self.icon_rect)

        if not self.open:
            return

        self._draw_panel_bg()

        # Title
        title_surf = self.font_large.render("SETTINGS", True, GOLD)
        self.panel_surf.blit(title_surf,
                             (PANEL_WIDTH // 2 - title_surf.get_width() // 2, 12))

        # Divider under title
        pygame.draw.line(self.panel_surf, (*GOLD_DIM, 160),
                         (16, 34), (PANEL_WIDTH - 16, 34), 1)

        # Sliders
        for slider in self.sliders:
            slider.draw(self.panel_surf, self.font_small)

        self.window.blit(self.panel_surf, (PANEL_X, PANEL_Y))