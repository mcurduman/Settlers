import pygame
from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH

WIDTH, HEIGHT = 1000, 700


class EndScreen:
    def __init__(self, screen, players, winner_name):
        """
        Initializes the EndScreen with player stats and winner information.
        """
        self.screen = screen
        self.players = players
        self.winner_name = winner_name
        self.font_title = pygame.font.Font(FONTS_PATH["extra_bold"], 64)
        self.font = pygame.font.Font(FONTS_PATH["bold"], 28)
        self.font_small = pygame.font.Font(FONTS_PATH["bold"], 20)
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill(PALETTE["bg_dark"])
        self.back_btn_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 100, 160, 50)

    def draw(self):
        """
        Draws the end screen, including winner, player stats, and back button.
        """
        self.screen.blit(self.bg, (0, 0))
        title = self.font_title.render("Game Over!", True, PALETTE["sand"])
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        if self.winner_name:
            winner_text = f"Winner: {self.winner_name}"
            winner_surf = self.font.render(winner_text, True, PALETTE["mint"])
            self.screen.blit(
                winner_surf, winner_surf.get_rect(center=(WIDTH // 2, 180))
            )
        else:
            no_winner_text = "No winner. Game exited early."
            no_winner_surf = self.font.render(no_winner_text, True, PALETTE["red"])
            self.screen.blit(
                no_winner_surf, no_winner_surf.get_rect(center=(WIDTH // 2, 180))
            )

        # Draw player stats
        y = 260
        for player in self.players:
            name = player["name"]
            vp = player["victory_points"]
            color = (
                PALETTE["mint"]
                if self.winner_name and name == self.winner_name
                else PALETTE["sand"]
            )
            player_text = f"{name}: {vp} Victory Points"
            surf = self.font_small.render(player_text, True, color)
            self.screen.blit(surf, surf.get_rect(center=(WIDTH // 2, y)))
            y += 50

        # Draw back button
        mouse = pygame.mouse.get_pos()
        hovered = self.back_btn_rect.collidepoint(mouse)
        btn_color = PALETTE["orange_dark"] if hovered else PALETTE["orange"]
        pygame.draw.rect(self.screen, btn_color, self.back_btn_rect, border_radius=12)
        pygame.draw.rect(
            self.screen, PALETTE["sand"], self.back_btn_rect, 2, border_radius=12
        )
        btn_text = self.font.render("BACK", True, PALETTE["bg_dark"])
        self.screen.blit(btn_text, btn_text.get_rect(center=self.back_btn_rect.center))

        pygame.display.flip()

    def run(self):
        """
        Main loop for the end screen. Handles drawing and user input for exit/back.
        """
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_btn_rect.collidepoint(event.pos):
                        return "back"
