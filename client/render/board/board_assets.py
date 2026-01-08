import pygame
from .board_constants import HEX_SIZE

_TILE_ICONS = {}


def load_tile_icons():
    """Load and cache tile icons for different resources."""
    global _TILE_ICONS
    if _TILE_ICONS:
        return _TILE_ICONS

    for res in ["sheep", "wheat", "brick", "wood", "desert"]:
        img = pygame.image.load(f"client/assets/tiles/{res}.png").convert_alpha()
        size = int(HEX_SIZE * 1.4)
        _TILE_ICONS[res] = pygame.transform.smoothscale(img, (size, size))

    return _TILE_ICONS
