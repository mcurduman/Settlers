import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH

WIDTH, HEIGHT = 1000, 700


class StartScreen:
    def __init__(self, screen):
        """
        Initializes the StartScreen with background, fonts, and button rects.
        """
        self.screen = screen

        self.font_title = pygame.font.Font(FONTS_PATH["extra_bold"], 64)
        self.font_btn = pygame.font.Font(FONTS_PATH["bold"], 32)

        self.bg = pygame.image.load("client/assets/backgrounds/start_2.png").convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        # Buttons
        btn_width = 320
        btn_height = 72
        center_x = WIDTH // 2 - btn_width // 2

        self.start_rect = pygame.Rect(center_x, 400, btn_width, btn_height)
        self.exit_rect = pygame.Rect(center_x, 500, btn_width, btn_height)

    def draw_button(self, rect, base_color, text, hover=False):
        color = tuple(min(255, c + 20) for c in base_color) if hover else base_color

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=14,
        )

        pygame.draw.rect(
            self.screen,
            PALETTE["sand"],
            rect,
            3,
            border_radius=14,
        )

        label = self.font_btn.render(text, True, PALETTE["bg_dark"])
        self.screen.blit(label, label.get_rect(center=rect.center))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            self.draw_screen()
            pygame.display.flip()

            result = self.handle_events()
            if result is not None:
                return result

    def draw_screen(self):
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
            title.get_rect(center=(WIDTH // 2, 200)),
        )

        start_hover = self.start_rect.collidepoint(mouse_pos)
        exit_hover = self.exit_rect.collidepoint(mouse_pos)

        self.draw_button(
            self.start_rect,
            PALETTE["mint"],
            "START",
            start_hover,
        )

        self.draw_button(
            self.exit_rect,
            PALETTE["orange_dark"],
            "EXIT",
            exit_hover,
        )

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        start_hover = self.start_rect.collidepoint(mouse_pos)
        exit_hover = self.exit_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "window_close"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_hover:
                    return "start"
                if exit_hover:
                    return "exit"

        return None
