import pygame
from engine.services.game_service import GameService
from client.render.board_renderer import draw_board
from client.render.panel_renderer import draw_panel
from client.input.interaction import handle_interaction
from client.assets.theme.fonts import FONTS_PATH

WIDTH, HEIGHT = 1000, 700
BOARD_WIDTH = int(WIDTH * 2 / 3)
PANEL_WIDTH = WIDTH - BOARD_WIDTH


class GameScreen:
    def __init__(self, screen, difficulty):
        self.screen = screen

        self.game = GameService()
        self.game.start_game(difficulty)
        self.state = self.game.get_state()
        self.last_state = (
            self.state.copy() if hasattr(self.state, "copy") else dict(self.state)
        )

        self.board_rect = pygame.Rect(0, 0, BOARD_WIDTH, HEIGHT)
        self.panel_rect = pygame.Rect(BOARD_WIDTH, 0, PANEL_WIDTH, HEIGHT)

        self.bg = pygame.image.load("client/assets/backgrounds/start_2.png").convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.ui = {
            "panel": {},
            "trade": {
                "give": None,
                "receive": None,
            },
            "trade_ui": {},
        }

        self.exit_btn_rect = pygame.Rect(0, 0, 0, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            handle_interaction(
                event,
                self.state,
                self.game,
                self.board_rect,
                self.ui["panel"],
                self.ui["trade_ui"],
                self.ui["trade"],
            )

            # EXIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.exit_btn_rect.collidepoint(event.pos):
                    self.game.end_game()
                    return True

    def update(self):
        try:
            new_state = self.game.get_state()
            self.last_state = (
                new_state.copy() if hasattr(new_state, "copy") else dict(new_state)
            )
        except Exception:
            # If game is not started, keep last known state
            new_state = self.last_state
        if new_state is not self.state:
            self.state = new_state
            if self.state.get("state") == "FinishedState":
                return "game_ended"

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        board_bg = pygame.Surface(self.board_rect.size, pygame.SRCALPHA)
        board_bg.fill((0, 0, 0, 120))
        self.screen.blit(board_bg, self.board_rect.topleft)
        draw_board(self.screen, self.state, self.board_rect)

        panel_bg = pygame.Surface(self.panel_rect.size)
        panel_bg.set_alpha(220)
        panel_bg.fill((0, 18, 25))
        self.screen.blit(panel_bg, self.panel_rect.topleft)

        self.ui["panel"], self.ui["trade_ui"] = draw_panel(
            self.screen, self.state, self.panel_rect, self.ui["trade"]
        )

        self.exit_btn_rect = pygame.Rect(
            self.panel_rect.x + self.panel_rect.width // 2 - 60,
            self.panel_rect.y + self.panel_rect.height - 60,
            120,
            40,
        )

        pygame.draw.rect(
            self.screen,
            (200, 40, 40),
            self.exit_btn_rect,
            border_radius=12,
        )
        pygame.draw.rect(
            self.screen,
            (60, 0, 0),
            self.exit_btn_rect,
            2,
            border_radius=12,
        )

        font_exit = pygame.font.Font(FONTS_PATH["bold"], 22)
        txt = font_exit.render("EXIT", True, (255, 255, 255))
        self.screen.blit(
            txt,
            txt.get_rect(center=self.exit_btn_rect.center),
        )

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)

            if self.handle_events():
                return {"exit_type": "exit_btn", "state": self.last_state}
            if self.update():
                return {"exit_type": "game_ended", "state": self.last_state}
            self.draw()

        return {"exit_type": "window_close", "state": self.last_state}
