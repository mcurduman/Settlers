import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH

WIDTH, HEIGHT = 1000, 700


class StartScreen:
    # EXIT button

    def __init__(self, screen):
        """
        Initializes the StartScreen with background, fonts, and button rects.
        """
        self.screen = screen

        self.font_title = pygame.font.Font(FONTS_PATH["extra_bold"], 64)

        self.font_btn = pygame.font.Font(FONTS_PATH["bold"], 30)

        self.bg = pygame.image.load("client/assets/backgrounds/start_2.png").convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        # Buttons
        btn_width = 320
        btn_height = 72
        center_x = WIDTH // 2 - btn_width // 2

        self.easy_rect = pygame.Rect(center_x, 360, btn_width, btn_height)
        self.hard_rect = pygame.Rect(center_x, 460, btn_width, btn_height)

        self.exit_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 80, 120, 44)

    def draw_button(self, rect, base_color, text, hover=False):
        """
        Draws a main menu button with optional hover effect.
        """
        color = tuple(min(255, c + 20) for c in base_color) if hover else base_color

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=14,
        )

        pygame.draw.rect(
            self.screen,
            (
                PALETTE["red"]
                if base_color == PALETTE["orange_dark"]
                else PALETTE["blue"]
            ),
            rect,
            3,
            border_radius=14,
        )

        if hover:
            pygame.draw.rect(
                self.screen,
                PALETTE["sand"],
                rect,
                4,
                border_radius=14,
            )

        label = self.font_btn.render(text, True, PALETTE["bg_dark"])
        self.screen.blit(label, label.get_rect(center=rect.center))

    def run(self):
        """
        Main loop for the start screen. Handles drawing and user input for menu selection.
        """
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.draw_screen()
            pygame.display.flip()
            result = self.handle_events()
            if result is not None:
                return result

    def draw_screen(self):
        """
        Draws the full start screen, including title and all buttons.
        """
        # Background
        self.screen.blit(self.bg, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        # Title
        title = self.font_title.render(
            "Mini Settlers",
            True,
            PALETTE["sand"],
        )
        self.screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, 180)),
        )

        # Hover detection
        easy_hover = self.easy_rect.collidepoint(mouse_pos)
        hard_hover = self.hard_rect.collidepoint(mouse_pos)
        exit_hover = self.exit_rect.collidepoint(mouse_pos)

        # Buttons
        self.draw_button(
            self.easy_rect,
            PALETTE["mint"],
            "EASY",
            easy_hover,
        )

        self.draw_button(
            self.hard_rect,
            PALETTE["orange_dark"],
            "HARD",
            hard_hover,
        )

        # EXIT BUTTON
        self.draw_exit_button(exit_hover)

    def draw_exit_button(self, hover):
        """
        Draws the EXIT button with hover effect.
        """
        pygame.draw.rect(
            self.screen,
            (200, 40, 40) if not hover else (220, 80, 80),
            self.exit_rect,
            border_radius=12,
        )
        pygame.draw.rect(self.screen, (60, 0, 0), self.exit_rect, 2, border_radius=12)
        font_exit = pygame.font.Font(FONTS_PATH["bold"], 22)
        txt = font_exit.render("EXIT", True, (255, 255, 255))
        self.screen.blit(txt, txt.get_rect(center=self.exit_rect.center))

    def handle_events(self):
        """
        Handles all pygame events for the start screen, including button clicks and exit.
        """
        mouse_pos = pygame.mouse.get_pos()
        easy_hover = self.easy_rect.collidepoint(mouse_pos)
        hard_hover = self.hard_rect.collidepoint(mouse_pos)
        exit_hover = self.exit_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "window_close"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_hover:
                    return "easy"
                if hard_hover:
                    return "hard"
                if exit_hover:
                    return "exit"
        return None
