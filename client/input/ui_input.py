import pygame


def handle_roll_and_main_state_ui(event, current_state, panel_ui, game):
    """
    Handles UI input for rolling dice and main action buttons during the game.
    Responds to left mouse button clicks on the roll button and main action buttons.
    Executes the appropriate game command based on the current state and button pressed.
    """
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return

    mouse = pygame.mouse.get_pos()

    # Roll
    if panel_ui.get("roll_button") and panel_ui["roll_button"].collidepoint(mouse):
        if current_state in {"SetupRollState", "PlayingRollState"}:
            game.execute_command_by_name("roll_dice")

    # Main actions
    if current_state == "PlayingMainState":
        handle_main_action_buttons(mouse, panel_ui, game)


def handle_main_action_buttons(mouse, panel_ui, game):
    """
    Handles clicks on main action buttons (settlement, road, trade, end turn).
    Executes the corresponding game command for the button pressed.
    """
    button_actions = [
        ("place_settlement_button", "start_place_settlement"),
        ("place_road_button", "start_place_road"),
        ("trade_with_bank_button", "start_trade_with_bank"),
        ("end_turn_button", "end_turn"),
    ]
    for button_key, command_name in button_actions:
        button = panel_ui.get(button_key)
        if button and button.collidepoint(mouse):
            game.execute_command_by_name(command_name)
            break


def handle_cancel_placement_ui(event, current_state, panel_ui, game):
    """
    Handles UI input for canceling placement actions (road or settlement).
    Responds to left mouse button clicks on the cancel button and exits the current placement state.
    """
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return

    mouse = pygame.mouse.get_pos()

    cancel_btn = panel_ui.get("cancel_placement_button")
    if cancel_btn and cancel_btn.collidepoint(mouse):
        if current_state == "PlayingPlaceRoadState":
            game.execute_command_by_name("exit_place_road")
        elif current_state == "PlayingPlaceSettlementState":
            game.execute_command_by_name("exit_place_settlement")
