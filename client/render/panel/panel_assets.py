import pygame

RESOURCE_ICONS = None


def load_resource_icons():
    """
    Loads and returns all resource icons as scaled pygame surfaces.
    """
    icons = {}
    for res in [
        "sheep",
        "wheat",
        "brick",
        "wood",
        "trophy",
        "longest_road",
        "road",
        "settlement",
    ]:
        img = pygame.image.load(f"client/assets/resources/{res}.png").convert_alpha()
        icons[res] = pygame.transform.smoothscale(img, (32, 32))
    return icons


def get_resource_icons():
    """
    Returns cached resource icons, loading them if necessary.
    """
    global RESOURCE_ICONS
    if RESOURCE_ICONS is None:
        RESOURCE_ICONS = load_resource_icons()
    return RESOURCE_ICONS
