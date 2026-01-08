import pygame
import math

from client.render.board.board_constants import NODE_RADIUS
from client.input.helpers import (
    point_near_segment,
    edge_connected_to_player,
    edge_connected_to_network,
    is_valid_settlement_node,
)
from client.render.coord import world_to_screen


def handle_setup_place_settlement(event, state, game, board_rect):
    """
    Handles mouse input for placing a settlement during the setup phase.
    Allows placement only on empty nodes when clicked.
    """
    mouse_pos = pygame.mouse.get_pos()

    for node in state["board"]["nodes"]:
        if node["owner"] is not None:
            continue

        screen_pos = world_to_screen(node["position"], board_rect)

        if math.dist(mouse_pos, screen_pos) <= NODE_RADIUS + 6:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.execute_command_by_name(
                    "place_settlement", position=node["position"]
                )
                return


def handle_playing_place_settlement(event, state, game, board_rect):
    """
    Handles mouse input for placing a settlement during the main phase.
    Only allows placement on valid nodes (distance rule, connected to road).
    """
    mouse_pos = pygame.mouse.get_pos()
    board = state["board"]
    current_player = state["current_player"]

    for node in board["nodes"]:
        if node["owner"] is not None:
            continue

        if not is_valid_settlement_node(board, node, current_player):
            continue

        screen_pos = world_to_screen(node["position"], board_rect)

        if math.dist(mouse_pos, screen_pos) <= NODE_RADIUS + 6:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.execute_command_by_name(
                    "place_settlement", position=node["position"]
                )
                return


def handle_setup_place_road(event, state, game, board_rect):
    """
    Handles mouse input for placing a road during the setup phase.
    Only allows placement on empty edges connected to the player's settlement or road.
    """
    mouse_pos = pygame.mouse.get_pos()
    board = state["board"]

    for edge in board["edges"]:
        if edge["owner"] is not None:
            continue

        if not edge_connected_to_player(
            edge, board, str(state["current_player"]).lower()
        ):
            continue

        a = world_to_screen(edge["a"], board_rect)
        b = world_to_screen(edge["b"], board_rect)

        if point_near_segment(mouse_pos, a, b, tolerance=14):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.execute_command_by_name("place_road", a=edge["a"], b=edge["b"])
                return


def handle_playing_place_road(event, state, game, board_rect):
    """
    Handles mouse input for placing a road during the main phase.
    Only allows placement on empty edges connected to the player's road network or settlement.
    """
    mouse_pos = pygame.mouse.get_pos()
    board = state["board"]
    current_player = str(state["current_player"]).lower()

    for edge in board["edges"]:
        if edge["owner"] is not None:
            continue

        if not edge_connected_to_network(edge, board, current_player):
            continue

        a = world_to_screen(edge["a"], board_rect)
        b = world_to_screen(edge["b"], board_rect)

        if point_near_segment(mouse_pos, a, b, tolerance=14):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.execute_command_by_name("place_road", a=edge["a"], b=edge["b"])
                return
