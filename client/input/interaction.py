import pygame
import math
from client.render.board_renderer import NODE_RADIUS
from client.input.helpers import (
    point_near_segment,
    edge_connected_to_player,
    edge_connected_to_network,
    is_valid_settlement_node,
)
from client.render.coord import world_to_screen


def handle_interaction(
    event, state, game, board_rect, panel_ui=None, trade_ui=None, trade_state=None
):
    """
    Main interaction handler that routes events based on the current game state.
    """
    current_state = state["state"]
    panel_ui = panel_ui or {}

    if current_state == "SetupPlaceSettlementState":
        handle_setup_place_settlement(event, state, game, board_rect)

    elif current_state == "SetupPlaceRoadState":
        handle_setup_place_road(event, state, game, board_rect)

    elif current_state in ("PlayingMainState", "SetupRollState", "PlayingRollState"):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            handle_roll_button(current_state, panel_ui, mouse, game)

            if current_state == "PlayingMainState":
                handle_main_state_buttons(panel_ui, mouse, game)

    elif current_state in ("PlayingPlaceRoadState", "PlayingPlaceSettlementState"):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if panel_ui.get("cancel_placement_button") and panel_ui[
                "cancel_placement_button"
            ].collidepoint(mouse):
                handle_cancel_placement_button(current_state, game)

        if current_state == "PlayingPlaceRoadState":
            handle_playing_place_road(event, state, game, board_rect)

        if current_state == "PlayingPlaceSettlementState":
            handle_playing_place_settlement(event, state, game, board_rect)

    elif current_state == "PlayingTradeWithBankState":
        handle_trade_with_bank(event, game, trade_ui, trade_state)


def handle_roll_button(current_state, panel_ui, mouse, game):
    """
    Handle the roll button interaction in Roll states.
    """
    if panel_ui.get("roll_button") and panel_ui["roll_button"].collidepoint(mouse):
        if current_state in {"SetupRollState", "PlayingRollState"}:
            game.execute_command_by_name("roll_dice")


def handle_main_state_buttons(panel_ui, mouse, game):
    """
    Handle the main state buttons interactions like:
    - Place Settlement
    - Place Road
    - Trade with Bank
    - End Turn
    """
    if panel_ui.get("place_settlement_button") and panel_ui[
        "place_settlement_button"
    ].collidepoint(mouse):
        game.execute_command_by_name("start_place_settlement")

    elif panel_ui.get("place_road_button") and panel_ui[
        "place_road_button"
    ].collidepoint(mouse):
        game.execute_command_by_name("start_place_road")

    elif panel_ui.get("trade_with_bank_button") and panel_ui[
        "trade_with_bank_button"
    ].collidepoint(mouse):
        game.execute_command_by_name("start_trade_with_bank")

    elif panel_ui.get("end_turn_button") and panel_ui["end_turn_button"].collidepoint(
        mouse
    ):
        game.execute_command_by_name("end_turn")


def handle_setup_place_settlement(event, state, game, board_rect):
    """
    Handle interactions in the SetupPlaceSettlementState.
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
    Handle interactions in the PlayingPlaceSettlementState.
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
    Handle interactions in the SetupPlaceRoadState.
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
    Handle interactions in the PlayingPlaceRoadState.
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


def handle_trade_with_bank(event, game, trade_ui, trade_state):
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return

    mouse = pygame.mouse.get_pos()

    for res, rect in trade_ui.get("trade_give", {}).items():
        if rect.collidepoint(mouse):
            trade_state["give"] = res

    for res, rect in trade_ui.get("trade_receive", {}).items():
        if rect.collidepoint(mouse):
            trade_state["receive"] = res

    if trade_ui.get("confirm_trade") and trade_ui["confirm_trade"].collidepoint(mouse):
        if trade_state["give"] and trade_state["receive"]:
            game.execute_command_by_name(
                "trade_with_bank",
                give=trade_state["give"],
                receive=trade_state["receive"],
            )
            trade_state["give"] = None
            trade_state["receive"] = None

    if trade_ui.get("cancel_trade") and trade_ui["cancel_trade"].collidepoint(mouse):
        trade_state["give"] = None
        trade_state["receive"] = None
        game.execute_command_by_name("exit_trade_with_bank")


def handle_cancel_placement_button(current_state, game):
    """
    Handle cancel placement button depending on the current state.
    """
    if current_state == "PlayingPlaceRoadState":
        game.execute_command_by_name("exit_place_road")
    elif current_state == "PlayingPlaceSettlementState":
        game.execute_command_by_name("exit_place_settlement")
