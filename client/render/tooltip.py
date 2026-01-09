import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH


def draw_tooltip(screen, text, mouse_pos):
    """
    Draws a tooltip with the given text at the mouse position, clamped to the screen.
    """
    font = pygame.font.Font(FONTS_PATH["bold"], 14)
    padding = 6
    offset = 12

    txt = font.render(text, True, PALETTE["sand"])
    bg_rect = txt.get_rect()

    x = mouse_pos[0] + offset
    y = mouse_pos[1] + offset

    bg_rect.topleft = (x, y)
    bg_rect.inflate_ip(padding * 2, padding * 2)

    screen_w, screen_h = screen.get_size()

    if bg_rect.right > screen_w:
        bg_rect.right = screen_w - 4

    if bg_rect.left < 0:
        bg_rect.left = 4

    # CLAMP VERTICAL
    if bg_rect.bottom > screen_h:
        bg_rect.bottom = screen_h - 4

    if bg_rect.top < 0:
        bg_rect.top = 4

    pygame.draw.rect(screen, PALETTE["bg_dark"], bg_rect, border_radius=6)
    pygame.draw.rect(screen, PALETTE["blue"], bg_rect, 2, border_radius=6)

    screen.blit(txt, txt.get_rect(center=bg_rect.center))
