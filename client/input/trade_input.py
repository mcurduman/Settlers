import pygame


def handle_trade_with_bank(event, game, trade_ui, trade_state):
    """
    Handles UI input for trading with the bank.
    Responds to left mouse button clicks on resource selection and confirm/cancel buttons.
    """
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
