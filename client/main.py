import pygame

from client.screens.start_screen import StartScreen
from client.screens.game_screen import GameScreen

# ----------------------------
# WINDOW CONFIG
# ----------------------------
WIDTH, HEIGHT = 1000, 700
BG_COLOR = (15, 23, 42)


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Settlers")

    while True:
        # ----------------------------
        # START SCREEN
        # ----------------------------
        start_screen = StartScreen(screen)
        difficulty = start_screen.run()

        # User closed window on start screen
        if difficulty is None or difficulty == "exit":
            break

        # ----------------------------
        # GAME SCREEN
        # ----------------------------
        game_screen = GameScreen(screen, difficulty)
        exit_main_screen = game_screen.run()

        if exit_main_screen:
            continue
        else:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
