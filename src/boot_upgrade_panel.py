import pygame

# Star wars colors
GOLD = (200, 160, 50)
GOLD_DIM = (140, 110, 35)
DARK_BG = (10, 8, 5)
PANEL_BORDER = (180, 140, 40)
TEXT_WHITE = (230, 220, 190)
PANEL_ALPHA = 210
BORDER_RADIUS = 6
BORDER_THICKNESS = 2

# Button colors
BTN_AFFORDABLE     = (180, 140, 40)   # gold — can afford
BTN_AFFORDABLE_HOV = (220, 175, 55)   # brighter gold on hover
BTN_DISABLED       = (50, 45, 35)     # dark grey — can't afford
BTN_TEXT_ON        = (10, 8, 5)       # dark text on gold button
BTN_TEXT_OFF       = (100, 90, 70)    # muted text on disabled button

# Panel dimensions
PANEL_WIDTH  = 280
PANEL_HEIGHT = 200
PANEL_X      = 16
PANEL_Y      = 700 - PANEL_HEIGHT - 16   # 16px from bottom of 700px window

# Button dimensions (inside the panel)
BTN_X      = 16
BTN_Y      = PANEL_HEIGHT - 52
BTN_WIDTH  = PANEL_WIDTH - 32
BTN_HEIGHT = 36


class BootUpgradePanel:
    def __init__(self, window):
        self.window = window
        self.panel_surf = pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT), pygame.SRCALPHA)

        # Hover state for button
        self.btn_hovering = False

        # Fonts
        try:
            self.font_title  = pygame.font.Font("assets/fonts/starjedi.ttf", 16)
            self.font_label  = pygame.font.Font("assets/fonts/starjedi.ttf", 13)
            self.font_value  = pygame.font.Font("assets/fonts/starjedi.ttf", 18)
            self.font_btn    = pygame.font.Font("assets/fonts/starjedi.ttf", 14)
        except (FileNotFoundError, pygame.error):
            self.font_title  = pygame.font.SysFont("Georgia", 16, bold=True)
            self.font_label  = pygame.font.SysFont("Georgia", 13, italic=True)
            self.font_value  = pygame.font.SysFont("Georgia", 18, bold=True)
            self.font_btn    = pygame.font.SysFont("Georgia", 14, bold=True)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_btn_rect_abs(self):
        """Upgrade button rect in window coordinates."""
        return pygame.Rect(PANEL_X + BTN_X, PANEL_Y + BTN_Y, BTN_WIDTH, BTN_HEIGHT)

    def _draw_panel_bg(self):
        """Dark semi-transparent background with gold border."""
        self.panel_surf.fill((0, 0, 0, 0))
        bg_rect = pygame.Rect(0, 0, PANEL_WIDTH, PANEL_HEIGHT)
        pygame.draw.rect(self.panel_surf, (*DARK_BG, PANEL_ALPHA),
                         bg_rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.panel_surf, (*PANEL_BORDER, 255),
                         bg_rect, width=BORDER_THICKNESS,
                         border_radius=BORDER_RADIUS)
        # Inner highlight line
        pygame.draw.line(self.panel_surf, (*GOLD, 80),
                         (BORDER_RADIUS, BORDER_THICKNESS + 2),
                         (PANEL_WIDTH - BORDER_RADIUS, BORDER_THICKNESS + 2), 1)

    def _draw_divider(self, y):
        pygame.draw.line(self.panel_surf, (*GOLD_DIM, 160),
                         (16, y), (PANEL_WIDTH - 16, y), 1)

    def _draw_stat_row(self, label, value, y):
        """Draw a label on the left and a value on the right."""
        label_surf = self.font_label.render(label, True, GOLD_DIM)
        value_surf = self.font_value.render(str(value), True, GOLD)
        self.panel_surf.blit(label_surf, (16, y))
        self.panel_surf.blit(value_surf, (PANEL_WIDTH - value_surf.get_width() - 16, y - 2))

    def _draw_button(self, can_afford):
        """Draw the upgrade button, greyed out if unaffordable."""
        btn_rect = pygame.Rect(BTN_X, BTN_Y, BTN_WIDTH, BTN_HEIGHT)

        if can_afford:
            color = BTN_AFFORDABLE_HOV if self.btn_hovering else BTN_AFFORDABLE
            text_color = BTN_TEXT_ON
            label = "UPGRADE BOOT"
        else:
            color = BTN_DISABLED
            text_color = BTN_TEXT_OFF
            label = "UPGRADE BOOT"

        pygame.draw.rect(self.panel_surf, color, btn_rect,
                         border_radius=BORDER_RADIUS)
        pygame.draw.rect(self.panel_surf, (*PANEL_BORDER, 180 if can_afford else 60),
                         btn_rect, width=BORDER_THICKNESS,
                         border_radius=BORDER_RADIUS)

        btn_surf = self.font_btn.render(label, True, text_color)
        bx = BTN_X + BTN_WIDTH  // 2 - btn_surf.get_width()  // 2
        by = BTN_Y + BTN_HEIGHT // 2 - btn_surf.get_height() // 2
        self.panel_surf.blit(btn_surf, (bx, by))

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def handle_event(self, event, player):
        """
        Call this inside your event loop, passing in the player.
        Returns True if an upgrade was successfully purchased.
        """
        if event.type == pygame.MOUSEMOTION:
            self.btn_hovering = self._get_btn_rect_abs().collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            can_afford = player.credits >= player.get_upgrade_cost()
            if can_afford and self._get_btn_rect_abs().collidepoint(event.pos):
                player.upgrade_boot()
                return True

        return False

    def draw(self, player):
        """Draw the full upgrade panel. Call once per frame in your draw method."""
        can_afford = player.credits >= player.get_upgrade_cost()

        self._draw_panel_bg()

        # Title
        title_surf = self.font_title.render("BOOT UPGRADE", True, GOLD)
        self.panel_surf.blit(title_surf,
                             (PANEL_WIDTH // 2 - title_surf.get_width() // 2, 12))

        self._draw_divider(34)

        # Stat rows
        self._draw_stat_row("BOOT LEVEL",   f"LVL {player.boot_level}",      46)
        self._draw_divider(72)
        self._draw_stat_row("PER KICK",     f"{player.kick_power} CR",        84)
        self._draw_divider(110)
        self._draw_stat_row("UPGRADE COST", f"{player.get_upgrade_cost()} CR", 122)

        self._draw_divider(148)

        # Upgrade button
        self._draw_button(can_afford)

        self.window.blit(self.panel_surf, (PANEL_X, PANEL_Y))