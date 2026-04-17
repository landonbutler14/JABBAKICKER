import pygame

# HUD Colors — Star Wars palette
GOLD = (200, 160, 50)
GOLD_DIM = (140, 110, 35)
DARK_BG = (10, 8, 5)
PANEL_BORDER = (180, 140, 40)
TEXT_WHITE = (230, 220, 190)  # Slightly warmish white

PANEL_WIDTH = 280
PANEL_HEIGHT = 120
PANEL_X = 1200 - PANEL_WIDTH - 16  # 16px from right edge
PANEL_Y = 16                        # 16px from top edge
BORDER_RADIUS = 6
BORDER_THICKNESS = 2
PANEL_ALPHA = 210                   # Semi-transparent


class HUD:
    def __init__(self, window):
        self.window = window

        # --- Fonts ---
        
        self.font_large = pygame.font.Font("assets/fonts/starjedi.ttf", 22)
        self.font_small = pygame.font.Font("assets/fonts/starjedi.ttf", 14)
        

        # --- Panel surface (semi-transparent background) ---
        self.panel = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT), pygame.SRCALPHA)

    def _draw_panel(self):
        """Draw the dark semi-transparent background with a gold border."""
        self.panel.fill((0, 0, 0, 0))  # Clear

        # Dark fill
        bg_rect = pygame.Rect(0, 0, PANEL_WIDTH, PANEL_HEIGHT)
        pygame.draw.rect(
            self.panel,
            (*DARK_BG, PANEL_ALPHA),
            bg_rect,
            border_radius=BORDER_RADIUS
        )

        # Gold border
        pygame.draw.rect(
            self.panel,
            (*PANEL_BORDER, 255),
            bg_rect,
            width=BORDER_THICKNESS,
            border_radius=BORDER_RADIUS
        )

        # Subtle inner highlight line along the top
        pygame.draw.line(
            self.panel,
            (*GOLD, 80),
            (BORDER_RADIUS, BORDER_THICKNESS + 2),
            (PANEL_WIDTH - BORDER_RADIUS, BORDER_THICKNESS + 2),
            1
        )

    def _draw_divider(self, y):
        """Draw a thin gold divider line inside the panel."""
        pygame.draw.line(
            self.panel,
            (*GOLD_DIM, 160),
            (16, y),
            (PANEL_WIDTH - 16, y),
            1
        )

    def draw(self, player):
        """Draw the HUD panel with current player stats."""
        self._draw_panel()

        # --- Title ---
        title_surf = self.font_small.render("JABBA KICKER", True, GOLD)
        self.panel.blit(title_surf, (PANEL_WIDTH // 2 - title_surf.get_width() // 2, 10))

        self._draw_divider(32)

        # --- Credits ---
        credits_label = self.font_small.render("CREDITS", True, GOLD_DIM)
        credits_value = self.font_large.render(f"{player.credits:,}", True, GOLD)

        self.panel.blit(credits_label, (16, 40))
        self.panel.blit(credits_value, (PANEL_WIDTH - credits_value.get_width() - 16, 37))

        self._draw_divider(68)

        # --- Credits per kick ---
        cpk_label = self.font_small.render("PER KICK", True, GOLD_DIM)
        cpk_value = self.font_large.render(f"{player.kick_power:,}", True, TEXT_WHITE)

        self.panel.blit(cpk_label, (16, 76))
        self.panel.blit(cpk_value, (PANEL_WIDTH - cpk_value.get_width() - 16, 73))

        # --- Blit panel onto window ---
        self.window.blit(self.panel, (PANEL_X, PANEL_Y))