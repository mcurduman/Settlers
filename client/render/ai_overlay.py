import pygame

from client.assets.theme.fonts import FONTS_PATH


def draw_ai_action(screen, text):
    """
    Draws an overlay at the bottom left of the screen showing the AI's current action.
    """
    font = pygame.font.Font(FONTS_PATH["regular"], 16)

    padding = 10
    margin = 8

    rendered = font.render(text, True, (230, 230, 230))
    bg_rect = rendered.get_rect()

    bg_rect.bottomleft = (
        margin + padding,
        screen.get_height() - margin - padding,
    )

    background = pygame.Surface(
        (bg_rect.width + padding * 2, bg_rect.height + padding * 2),
        pygame.SRCALPHA,
    )
    background.fill((0, 0, 0, 160))  # semi-transparent

    screen.blit(
        background,
        (bg_rect.x - padding, bg_rect.y - padding),
    )
    screen.blit(rendered, bg_rect)
