import pygame

from client.assets.theme.colors import PALETTE
from client.render.panel.buttons import draw_cancel_button
from client.render.panel.panel_actions import draw_panel_action_buttons
from client.render.panel.panel_header import draw_panel_header
from client.render.panel.player_card import draw_player_card
from client.render.panel.trade_panel import draw_trade_with_bank_panel
from client.render.tooltip import draw_tooltip


def draw_panel(screen, state, rect, trade_state):
    """
    Main panel orchestrator.
    Responsible only for layout & delegation.
    """

    pygame.draw.rect(screen, PALETTE["bg_dark"], rect)

    panel_ui = {}
    trade_ui = None

    x = rect.x + 16
    y = rect.y + 16
    width = rect.width - 32

    # ---- PANEL HEADER ----
    y = draw_panel_header(screen, state, x, y)

    hovered_tooltip = None

    # ---- PLAYER CARDS ----
    for player in state["players"]:
        if (
            state["state"] == "PlayingTradeWithBankState"
            and str(player["name"]).lower() != "human"
        ):
            continue
        y, roll_btn, player_tooltip = draw_player_card(
            screen,
            state,
            player,
            state["current_player"],
            x,
            y,
            width,
        )

        if roll_btn:
            panel_ui["roll_button"] = roll_btn

        if player_tooltip:
            hovered_tooltip = player_tooltip

        y += 12

    # ---- MAIN ACTION BUTTONS ----
    if state["state"] == "PlayingMainState":
        hovered_tooltip = draw_panel_action_buttons(
            screen,
            state,
            x,
            y,
            width,
            panel_ui,
            hovered_tooltip,
        )
        if hovered_tooltip:
            draw_tooltip(screen, hovered_tooltip[0], hovered_tooltip[1])

    # ---- TRADE PANEL ----
    if state["state"] == "PlayingTradeWithBankState":
        trade_ui, _ = draw_trade_with_bank_panel(
            screen,
            state,
            rect,
            trade_state,
            hovered_tooltip,
        )
        return panel_ui, trade_ui

    # ---- CANCEL PLACEMENT ----
    if state["state"] in (
        "PlayingPlaceRoadState",
        "PlayingPlaceSettlementState",
    ):
        panel_ui["cancel_placement_button"] = draw_cancel_button(
            screen, rect, tooltip="Cancel placement"
        )

    return panel_ui, trade_ui
