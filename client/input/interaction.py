from .ui_input import handle_roll_and_main_state_ui, handle_cancel_placement_ui
from .board_input import (
    handle_setup_place_settlement,
    handle_setup_place_road,
    handle_playing_place_settlement,
    handle_playing_place_road,
)
from .trade_input import handle_trade_with_bank


def handle_interaction(
    event, state, game, board_rect, panel_ui=None, trade_ui=None, trade_state=None
):
    """
    Main input orchestrator. Dispatches the event to the correct handler based on the current game state.
    - For setup states, delegates to board input handlers.
    - For main/roll states, delegates to UI input handlers.
    - For placement states, handles cancel and board input.
    - For trade state, delegates to trade input handler.

    Args:
        event: pygame event
        state: current game state dict
        game: GameService instance
        board_rect: pygame.Rect for board
        panel_ui: UI elements for panel (optional)
        trade_ui: UI elements for trade (optional)
        trade_state: trade state dict (optional)
    """
    current_state = state["state"]
    panel_ui = panel_ui or {}

    if current_state == "SetupPlaceSettlementState":
        handle_setup_place_settlement(event, state, game, board_rect)

    elif current_state == "SetupPlaceRoadState":
        handle_setup_place_road(event, state, game, board_rect)

    elif current_state in ("PlayingMainState", "SetupRollState", "PlayingRollState"):
        handle_roll_and_main_state_ui(event, current_state, panel_ui, game)

    elif current_state in ("PlayingPlaceRoadState", "PlayingPlaceSettlementState"):
        handle_cancel_placement_ui(event, current_state, panel_ui, game)

        if current_state == "PlayingPlaceRoadState":
            handle_playing_place_road(event, state, game, board_rect)

        if current_state == "PlayingPlaceSettlementState":
            handle_playing_place_settlement(event, state, game, board_rect)

    elif current_state == "PlayingTradeWithBankState":
        handle_trade_with_bank(event, game, trade_ui, trade_state)
