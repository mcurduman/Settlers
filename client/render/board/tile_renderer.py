import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH
from client.assets.theme.resource_colors import RESOURCE_COLORS
from client.render.coord import axial_to_screen

from .board_constants import HEX_SIZE
from .board_geometry import hex_corners


def draw_tile(screen, tile, board_rect, icons):
    """
    Draws a single hex tile, its resource icon, and number token if present.
    Handles outline and icon rendering for the tile.
    """
    cx, cy = axial_to_screen(tile["q"], tile["r"], board_rect)

    resource = tile["resource"]
    number = tile["number"]

    color = RESOURCE_COLORS[resource]
    corners = hex_corners(cx, cy, HEX_SIZE)

    pygame.draw.polygon(screen, color, corners)
    pygame.draw.polygon(screen, PALETTE["bg_dark"], corners, 3)

    icon = icons.get(resource)
    if icon:
        icon_rect = icon.get_rect(center=(cx, cy))
        icon.set_alpha(120)
        screen.blit(icon, icon_rect)

    if number is not None:
        font = pygame.font.Font(FONTS_PATH["extra_bold"], 45)
        outline_color = (255, 255, 255)

        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx == 0 and dy == 0:
                    continue
                outline = font.render(str(number), True, outline_color)
                screen.blit(outline, outline.get_rect(center=(cx + dx, cy + dy)))

        txt = font.render(str(number), True, PALETTE["bg_dark"])
        screen.blit(txt, txt.get_rect(center=(cx, cy)))


def draw_tiles(screen, tiles, board_rect, icons):
    """
    Draws all hex tiles on the board by calling draw_tile for each.
    """
    for tile in tiles:
        draw_tile(screen, tile, board_rect, icons)
