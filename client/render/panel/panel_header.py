import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH

from .panel_constants import PHASE_NAMES, STATE_HELPER


def draw_panel_header(screen, state, x, y):
    """
    Draws the panel header: phase name, helper text, and error message if present.
    Returns the new y position after drawing.
    """
    font_title = pygame.font.Font(FONTS_PATH["bold"], 28)
    font = pygame.font.Font(FONTS_PATH["bold"], 15)

    phase = state["state"]
    screen.blit(
        font_title.render(PHASE_NAMES.get(phase, phase), True, PALETTE["sand"]),
        (x, y),
    )
    y += 35

    helper = STATE_HELPER.get(phase)
    if helper:
        screen.blit(font.render(helper, True, PALETTE["mint"]), (x, y))
        y += 34

    if state.get("error"):
        screen.blit(font.render(state["error"], True, PALETTE["red"]), (x, y))
        y += 28

    return y
