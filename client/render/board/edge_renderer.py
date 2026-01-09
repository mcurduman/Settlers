import pygame

from client.assets.theme.colors import PALETTE
from client.render.coord import world_to_screen
from client.render.render_helpers import (edge_connected_to_network,
                                          edge_connected_to_settlement)


def draw_unowned_edge(screen, edge, board, phase, current_player, a, b):
    is_valid = False
    if phase == "SetupPlaceRoadState":
        is_valid = edge_connected_to_settlement(edge, board, current_player)
    elif phase == "PlayingPlaceRoadState":
        is_valid = edge_connected_to_network(edge, board, current_player)

    if is_valid and current_player.lower() == "human":
        pygame.draw.line(screen, (255, 255, 255), a, b, 16)
        pygame.draw.line(screen, PALETTE["mint"], a, b, 10)
    else:
        pygame.draw.line(screen, PALETTE["mint"], a, b, 6)

def draw_owned_edge(screen, edge, a, b):
    owner = edge["owner"]
    color = PALETTE["ai"] if str(owner).lower() == "ai" else PALETTE["human"]
    pygame.draw.line(screen, color, a, b, 10)

def draw_edges(screen, edges, board, phase, current_player, board_rect):
    """
    Draws all board edges (roads and possible placements) for the current game state.
    Highlights valid placements and colors owned roads by player type.
    """
    for edge in edges:
        a = world_to_screen(edge["a"], board_rect)
        b = world_to_screen(edge["b"], board_rect)

        if edge.get("owner") is None:
            draw_unowned_edge(screen, edge, board, phase, current_player, a, b)
        else:
            draw_owned_edge(screen, edge, a, b)
