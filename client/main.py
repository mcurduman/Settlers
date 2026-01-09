import pygame

from client.screens.end_screen import EndScreen
from client.screens.game_screen import GameScreen
from client.screens.start_screen import StartScreen

WIDTH, HEIGHT = 1000, 700
BG_COLOR = (15, 23, 42)


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Settlers")

    running = True
    while running:

        start_screen = StartScreen(screen)
        difficulty = start_screen.run()

        if difficulty in (None, "exit", "window_close"):
            break

        game_screen = GameScreen(screen, difficulty)
        exit_info = game_screen.run()

        if exit_info["exit_type"] == "window_close":
            break

        state = exit_info.get("state", {})
        players = state.get("players", [])
        winner = state.get("winner")

        end_screen = EndScreen(
            screen,
            players,
            winner if winner and winner != "Unknown" else None,
        )
        end_screen.run()

    pygame.quit()


if __name__ == "__main__":
    main()
