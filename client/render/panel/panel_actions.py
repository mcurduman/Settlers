import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH
from engine.game.rules.cost import COSTS
from client.input.helpers import can_trade_3_1, has_resources
from client.render.render_helpers import has_valid_settlement_spot


def get_button_definitions(state, can_build_settlement, can_build_road, can_trade):
    """
    Returns the definitions for all action buttons based on the current state and available actions.
    """
    if state["state"] == "PlayingPlaceSettlementState":
        return [
            ("Cancel", "cancel_placement_button", True, "Cancel placing settlement")
        ]
    elif state["state"] == "PlayingPlaceRoadState":
        return [("Cancel", "cancel_placement_button", True, "Cancel placing road")]
    else:
        return [
            (
                "Place Settlement",
                "place_settlement_button",
                can_build_settlement,
                "Needs 1 brick, 1 wood, 1 sheep, 1 wheat",
            ),
            (
                "Place Road",
                "place_road_button",
                can_build_road,
                "Needs 1 brick, 1 wood",
            ),
            (
                "Trade with Bank",
                "trade_with_bank_button",
                can_trade,
                "Trade 3 of same resource for 1",
            ),
            ("End Turn", "end_turn_button", True, "End your turn"),
        ]


def _get_end_turn_button_colors(hovered):
    """
    Returns the background, border, and text color for the End Turn button.
    """
    bg = PALETTE["sand"] if hovered else PALETTE["yellow"]
    border = PALETTE["orange_dark"] if hovered else PALETTE["orange"]
    txt_color = PALETTE["bg_dark"]
    return bg, border, txt_color


def _get_cancel_placement_button_colors(hovered):
    """
    Returns the background, border, and text color for the Cancel Placement button.
    """
    bg = PALETTE["orange_dark"] if hovered else PALETTE["orange"]
    border = PALETTE["sand"] if hovered else PALETTE["orange_dark"]
    txt_color = PALETTE["bg_dark"]
    return bg, border, txt_color


def _get_default_button_colors(hovered):
    """
    Returns the background, border, and text color for default action buttons.
    """
    bg = PALETTE["mint"] if hovered else PALETTE["blue_dark"]
    border = PALETTE["sand"] if hovered else PALETTE["blue"]
    txt_color = PALETTE["bg_dark"]
    return bg, border, txt_color


def get_button_colors(key, enabled, hovered):
    """
    Returns the color tuple for a button based on its type, enabled state, and hover state.
    """
    if not enabled:
        return PALETTE["bg_dark"], PALETTE["blue"], PALETTE["blue"]
    if key == "end_turn_button":
        return _get_end_turn_button_colors(hovered)
    elif key == "cancel_placement_button":
        return _get_cancel_placement_button_colors(hovered)
    else:
        return _get_default_button_colors(hovered)


def draw_panel_action_buttons(
    screen, state, x, y, width, panel_ui, hovered_tooltip=None
):
    """
    Draws action buttons for the main playing state:
    - Place Settlement
    - Place Road
    - Trade with Bank
    - End Turn
    Also handles Cancel buttons for placement states.
    """

    current_player = next(
        p for p in state["players"] if p["name"] == state["current_player"]
    )

    hovered_tooltip_result = hovered_tooltip

    if current_player.get("is_ai"):
        return hovered_tooltip_result

    resources = current_player["resources"]

    can_build_settlement = has_resources(
        resources, COSTS["settlement"]
    ) and has_valid_settlement_spot(state["board"], current_player["name"])

    can_build_road = has_resources(resources, COSTS["road"])
    can_trade = can_trade_3_1(resources)

    btn_defs = get_button_definitions(
        state, can_build_settlement, can_build_road, can_trade
    )

    btn_w = (width - 16) // 2
    btn_h = 38
    gap = 16
    start_y = y + 10
    mouse = pygame.mouse.get_pos()

    btn_font = pygame.font.Font(FONTS_PATH["bold"], 14)

    for i, (label, key, enabled, tooltip) in enumerate(btn_defs):
        col = i % 2
        row = i // 2

        btn_x = x + col * (btn_w + gap)
        btn_y = start_y + row * (btn_h + gap)
        rect_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        hovered = rect_btn.collidepoint(mouse)

        bg, border, txt_color = get_button_colors(key, enabled, hovered)

        pygame.draw.rect(screen, bg, rect_btn, border_radius=10)
        pygame.draw.rect(screen, border, rect_btn, 2, border_radius=10)

        txt = btn_font.render(label, True, txt_color)
        screen.blit(txt, txt.get_rect(center=rect_btn.center))

        if enabled:
            panel_ui[key] = rect_btn

        if hovered:
            hovered_tooltip_result = (tooltip, mouse)

    return hovered_tooltip_result
