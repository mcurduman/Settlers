import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH
from client.render.tooltip import draw_tooltip


def draw_roll_button(screen, rect, enabled):
    """
    Draws the ROLL button and its tooltip if hovered and enabled.
    """
    mouse = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse)

    bg = PALETTE["mint"] if enabled else PALETTE["blue_dark"]
    border = PALETTE["sand"] if hovered and enabled else PALETTE["blue"]

    pygame.draw.rect(screen, bg, rect, border_radius=10)
    pygame.draw.rect(screen, border, rect, 2, border_radius=10)

    font = pygame.font.Font(FONTS_PATH["bold"], 16)
    label = font.render("ROLL", True, PALETTE["bg_dark"])
    screen.blit(label, label.get_rect(center=rect.center))

    if hovered and enabled:
        draw_tooltip(screen, "Roll the dice to continue", mouse)


def draw_cancel_button(screen, rect, tooltip="Cancel"):
    """
    Draws the CANCEL button and its tooltip if hovered.
    Returns the button rect for interaction.
    """
    btn_w = rect.width - 32
    btn_h = 42
    x = rect.x + 16
    y = rect.y + rect.height - btn_h - 80

    rect_btn = pygame.Rect(x, y, btn_w, btn_h)
    mouse = pygame.mouse.get_pos()
    hovered = rect_btn.collidepoint(mouse)

    bg = PALETTE["orange"]
    border = PALETTE["sand"] if hovered else PALETTE["orange_dark"]

    pygame.draw.rect(screen, bg, rect_btn, border_radius=12)
    pygame.draw.rect(screen, border, rect_btn, 2, border_radius=12)

    font = pygame.font.Font(FONTS_PATH["bold"], 16)
    txt = font.render("CANCEL", True, PALETTE["bg_dark"])
    screen.blit(txt, txt.get_rect(center=rect_btn.center))

    if hovered:
        draw_tooltip(screen, tooltip, mouse)

    return rect_btn
