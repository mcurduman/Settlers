import pygame
import math
from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH
from client.assets.theme.resource_colors import RESOURCE_COLORS
from client.render.coord import world_to_screen, axial_to_screen
from client.render.render_helpers import (
    edge_connected_to_settlement,
    edge_connected_to_network,
    is_valid_settlement_node,
)

HEX_SIZE = 100
NODE_RADIUS = 15

_TILE_ICONS = {}


def load_tile_icons():
    global _TILE_ICONS
    if _TILE_ICONS:
        return _TILE_ICONS

    for res in ["sheep", "wheat", "brick", "wood", "desert"]:
        img = pygame.image.load(f"client/assets/tiles/{res}.png").convert_alpha()
        size = int(HEX_SIZE * 1.4)
        _TILE_ICONS[res] = pygame.transform.smoothscale(img, (size, size))

    return _TILE_ICONS


def hex_corners(cx, cy, size):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        points.append((cx + size * math.cos(angle), cy + size * math.sin(angle)))
    return points


def draw_tile(screen, tile, board_rect, icons):
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


def draw_board(screen, state, board_rect):
    board = state["board"]
    phase = state.get("state", "")
    current_player = state.get("current_player", "")

    icons = load_tile_icons()

    _draw_tiles(screen, board["tiles"], board_rect, icons)
    _draw_edges(screen, board["edges"], board, phase, current_player, board_rect)
    _draw_nodes(screen, board["nodes"], phase, board_rect, board, current_player)


def _draw_tiles(screen, tiles, board_rect, icons):
    for tile in tiles:
        draw_tile(screen, tile, board_rect, icons)


def _draw_edges(screen, edges, board, phase, current_player, board_rect):
    for edge in edges:
        a = world_to_screen(edge["a"], board_rect)
        b = world_to_screen(edge["b"], board_rect)

        if edge.get("owner") is None:
            is_valid = False

            if phase == "SetupPlaceRoadState":
                is_valid = edge_connected_to_settlement(edge, board, current_player)
            elif phase == "PlayingPlaceRoadState":
                is_valid = edge_connected_to_network(edge, board, current_player)

            if is_valid:
                pygame.draw.line(screen, (255, 255, 255), a, b, 16)
                pygame.draw.line(screen, PALETTE["mint"], a, b, 10)
            else:
                pygame.draw.line(screen, PALETTE["mint"], a, b, 6)
        else:
            owner = edge["owner"]
            color = PALETTE["ai"] if str(owner).lower() == "ai" else PALETTE["human"]
            pygame.draw.line(screen, color, a, b, 10)


def _draw_nodes(screen, nodes, phase, board_rect, board=None, current_player=None):
    for node in nodes:
        pos = world_to_screen(node["position"], board_rect)

        if node["owner"] is None:
            if phase == "PlayingPlaceSettlementState":
                if is_valid_settlement_node(board, node, current_player):
                    pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS + 4)
                    pygame.draw.circle(screen, (255, 255, 255), pos, NODE_RADIUS + 6, 2)
                else:
                    pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)
            elif phase == "SetupPlaceSettlementState":
                pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)
                pygame.draw.circle(screen, (255, 255, 255), pos, NODE_RADIUS + 3, 3)
            else:
                pygame.draw.circle(screen, PALETTE["mint"], pos, NODE_RADIUS)

        elif str(node["owner"]).lower() == "ai":
            pygame.draw.circle(screen, PALETTE["ai"], pos, NODE_RADIUS)
        else:
            pygame.draw.circle(screen, PALETTE["human"], pos, NODE_RADIUS)
