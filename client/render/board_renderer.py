import pygame
import math
from client.assets.theme.colors import PALETTE
from client.assets.theme.resource_colors import RESOURCE_COLORS
from client.render.coord import world_to_screen
from client.render.coord import axial_to_screen

# CONFIG
HEX_SIZE = 100
SCALE = HEX_SIZE
NODE_RADIUS = 15

_TILE_ICONS = {}


def load_tile_icons():
    global _TILE_ICONS
    if _TILE_ICONS:
        return _TILE_ICONS

    for res in ["sheep", "wheat", "clay", "forest", "desert"]:
        img = pygame.image.load(f"client/assets/tiles/{res}.png").convert_alpha()

        # scale icon relativ la hex
        size = int(HEX_SIZE * 1.4)
        _TILE_ICONS[res] = pygame.transform.smoothscale(img, (size, size))

    return _TILE_ICONS


# HEX SHAPE
def hex_corners(cx, cy, size):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        points.append(
            (
                cx + size * math.cos(angle),
                cy + size * math.sin(angle),
            )
        )
    return points


# DRAW TILE
def draw_tile(screen, tile, board_rect, icons):
    cx, cy = axial_to_screen(tile["q"], tile["r"], board_rect)

    resource = tile["resource"]
    number = tile["number"]

    # background color
    color = RESOURCE_COLORS[resource]
    corners = hex_corners(cx, cy, HEX_SIZE)

    pygame.draw.polygon(screen, color, corners)
    pygame.draw.polygon(screen, PALETTE["bg_dark"], corners, 3)

    icon = icons.get(resource)
    if icon:
        icon_rect = icon.get_rect(center=(cx, cy))
        icon.set_alpha(120)  # subtle pattern look
        screen.blit(icon, icon_rect)

    if number is not None:
        font = pygame.font.Font("client/assets/fonts/Cinzel-ExtraBold.ttf", 45)
        outline_color = (255, 255, 255)
        text_str = str(number)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx == 0 and dy == 0:
                    continue
                outline = font.render(text_str, True, outline_color)
                rect = outline.get_rect(center=(cx + dx, cy + dy))
                screen.blit(outline, rect)
        txt = font.render(text_str, True, PALETTE["bg_dark"])
        screen.blit(txt, txt.get_rect(center=(cx, cy)))


# DRAW BOARD
def draw_board(screen, state, board_rect, hovered_node=None):
    board = state["board"]

    # ---- tiles (from axial coords)
    icons = load_tile_icons()
    for tile in board["tiles"]:
        draw_tile(screen, tile, board_rect, icons)

    # ---- edges (from world coords)
    phase = state.get("state", "")
    current_player = state.get("current_player", "")
    for edge in board["edges"]:
        a = world_to_screen(edge["a"], board_rect)
        b = world_to_screen(edge["b"], board_rect)
        if phase == "SetupPlaceRoadState" and edge.get("owner") is None:
            # Only highlight valid edges for current player
            valid_edge = False
            for node in board["nodes"]:
                if (
                    tuple(node["position"]) == tuple(edge["a"])
                    or tuple(node["position"]) == tuple(edge["b"])
                ) and str(node.get("owner", "")).lower() == current_player.lower():
                    valid_edge = True
                    break
            if valid_edge:
                pygame.draw.line(screen, (255, 255, 255), a, b, 16)  # white outline
                pygame.draw.line(screen, PALETTE["mint"], a, b, 10)
            else:
                pygame.draw.line(screen, PALETTE["mint"], a, b, 10)
        else:
            # Color by owner
            owner = edge.get("owner")
            if owner is None:
                color = PALETTE["mint"]
            elif str(owner).lower() == "ai":
                color = PALETTE["ai"]
            else:
                color = PALETTE["human"]
            pygame.draw.line(screen, color, a, b, 10)

    # ---- nodes (from world coords)
    phase = state.get("state", "")
    highlight_valid = phase in ("SetupPlaceSettlementState")
    for node in board["nodes"]:
        pos = world_to_screen(node["position"], board_rect)
        if node["owner"] is None:
            if highlight_valid:
                # Highlight valid nodes for placement
                pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)
                pygame.draw.circle(
                    screen, (255, 255, 255), pos, NODE_RADIUS + 3, 3
                )  # white outline
            else:
                pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)
        elif str(node["owner"]).lower() == "ai":
            pygame.draw.circle(screen, PALETTE["ai"], pos, NODE_RADIUS)
        else:
            pygame.draw.circle(screen, PALETTE["human"], pos, NODE_RADIUS)
