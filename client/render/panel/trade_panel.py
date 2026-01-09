import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH
from client.render.tooltip import draw_tooltip

from .panel_assets import get_resource_icons


def get_button_state(mode, resources, trade_state, res):
    """
    Determines if a trade button is enabled, selected, or same as the other resource.
    """
    if mode == "give":
        enabled = resources.get(res, 0) >= 3
        selected = trade_state["give"] == res
        is_same = False
    else:
        enabled = True
        is_same = trade_state["give"] == res
        selected = trade_state["receive"] == res
    return enabled, selected, is_same


def get_give_button_colors(enabled, selected, hovered):
    """
    Returns color and alpha for a 'give' resource button based on state.
    """
    if not enabled:
        bg = PALETTE["bg_dark"]
        border = PALETTE["blue"]
        alpha = 80
    else:
        bg = PALETTE["orange"] if selected else PALETTE["mint"]
        border = PALETTE["sand"] if hovered else PALETTE["blue"]
        alpha = 255
    return bg, border, alpha


def get_receive_button_colors(is_same, selected, hovered):
    """
    Returns color and alpha for a 'receive' resource button based on state.
    """
    if is_same:
        bg = PALETTE["bg_dark"]
        border = PALETTE["blue"]
        alpha = 80
    else:
        bg = PALETTE["orange"] if selected else PALETTE["blue_dark"]
        border = PALETTE["sand"] if hovered else PALETTE["blue"]
        alpha = 255
    return bg, border, alpha


def get_button_colors(mode, enabled, selected, is_same, hovered):
    """
    Returns the color tuple for a button based on mode and state.
    """
    if mode == "give":
        return get_give_button_colors(enabled, selected, hovered)
    else:
        return get_receive_button_colors(is_same, selected, hovered)


def handle_panel_ui(panel_ui, mode, enabled, is_same, res, rect_btn):
    """
    Updates the panel_ui dictionary with the button rect if it should be interactive.
    """
    if mode == "give" and enabled:
        panel_ui["trade_give"][res] = rect_btn
    elif mode == "receive" and not is_same:
        panel_ui["trade_receive"][res] = rect_btn


def handle_tooltip(screen, mode, enabled, is_same, res, mouse):
    """
    Draws the appropriate tooltip for a trade resource button.
    """
    if mode == "give":
        draw_tooltip(
            screen,
            f"Give 3 {res}" if enabled else f"Need at least 3 {res}",
            mouse,
        )
    else:
        draw_tooltip(
            screen,
            "Cannot receive same resource" if is_same else f"Receive 1 {res}",
            mouse,
        )


def draw_resource_buttons(
    screen,
    resource_icons,
    resources,
    trade_state,
    mouse,
    x,
    y,
    width,
    row_h,
    gap,
    panel_ui,
    mode,
):
    """
    Draws all resource buttons for trading (give or receive) and handles tooltips.
    Returns the new y position after drawing.
    """
    btn_w = (width - 80) // 4
    bx = x + 60
    for res in ["sheep", "wheat", "brick", "wood"]:
        enabled, selected, is_same = get_button_state(mode, resources, trade_state, res)
        rect_btn = pygame.Rect(bx, y, btn_w, row_h)
        hovered = rect_btn.collidepoint(mouse)
        bg, border, alpha = get_button_colors(mode, enabled, selected, is_same, hovered)

        pygame.draw.rect(screen, bg, rect_btn, border_radius=8)
        pygame.draw.rect(screen, border, rect_btn, 2, border_radius=8)

        icon = resource_icons[res].copy()
        icon.set_alpha(alpha)
        screen.blit(icon, icon.get_rect(center=rect_btn.center))

        handle_panel_ui(panel_ui, mode, enabled, is_same, res, rect_btn)

        if hovered:
            handle_tooltip(screen, mode, enabled, is_same, res, mouse)
        bx += btn_w + gap
    return y + row_h + (gap if mode == "give" else gap * 2)


def draw_action_buttons(screen, font, panel_ui, trade_state, rect, y, mouse):
    """
    Draws the confirm and cancel action buttons for the trade panel, with tooltips.
    """
    confirm_enabled = (
        trade_state["give"]
        and trade_state["receive"]
        and trade_state["give"] != trade_state["receive"]
    )

    btn_w_action = 140
    btn_h_action = 40
    cx = rect.centerx - btn_w_action - 10
    rx = rect.centerx + 10

    confirm_rect = pygame.Rect(cx, y, btn_w_action, btn_h_action)
    cancel_rect = pygame.Rect(rx, y, btn_w_action, btn_h_action)

    if confirm_enabled:
        bg = PALETTE["mint"]
        border = PALETTE["sand"]
        txt_color = PALETTE["bg_dark"]
    else:
        bg = PALETTE["bg_dark"]
        border = PALETTE["blue"]
        txt_color = PALETTE["blue"]

    pygame.draw.rect(screen, bg, confirm_rect, border_radius=10)
    pygame.draw.rect(screen, border, confirm_rect, 2, border_radius=10)
    screen.blit(
        font.render("CONFIRM", True, txt_color),
        font.render("CONFIRM", True, txt_color).get_rect(center=confirm_rect.center),
    )

    if confirm_enabled:
        panel_ui["confirm_trade"] = confirm_rect
    if confirm_rect.collidepoint(mouse):
        draw_tooltip(
            screen,
            "Confirm trade" if confirm_enabled else "Select resources first",
            mouse,
        )

    # CANCEL
    pygame.draw.rect(screen, PALETTE["orange"], cancel_rect, border_radius=12)
    pygame.draw.rect(
        screen,
        PALETTE["sand"] if cancel_rect.collidepoint(mouse) else PALETTE["orange_dark"],
        cancel_rect,
        2,
        border_radius=12,
    )
    screen.blit(
        font.render("CANCEL", True, PALETTE["bg_dark"]),
        font.render("CANCEL", True, PALETTE["bg_dark"]).get_rect(
            center=cancel_rect.center
        ),
    )

    panel_ui["cancel_trade"] = cancel_rect
    if cancel_rect.collidepoint(mouse):
        draw_tooltip(screen, "Cancel trade", mouse)


def draw_trade_with_bank_panel(screen, state, rect, trade_state, hovered_tooltip=None):
    """
    Draws the full trade with bank panel, including resource and action buttons.
    Returns the panel_ui dictionary and hovered_tooltip.
    """
    RESOURCE_ICONS = get_resource_icons()

    panel_ui = {
        "trade_give": {},
        "trade_receive": {},
        "confirm_trade": None,
        "cancel_trade": None,
    }

    mouse = pygame.mouse.get_pos()
    current_player = next(
        p for p in state["players"] if p["name"] == state["current_player"]
    )
    resources = current_player["resources"]

    padding = 16
    row_h = 36
    gap = 8

    x = rect.x + padding
    y = rect.y + 260
    width = rect.width - padding * 2

    font_title = pygame.font.Font(FONTS_PATH["bold"], 18)
    font = pygame.font.Font(FONTS_PATH["bold"], 14)

    # ---- TITLE ----
    screen.blit(
        font_title.render("Trade with Bank (3:1)", True, PALETTE["sand"]),
        (x, y),
    )
    y += row_h

    # ---- GIVE ----
    screen.blit(font.render("Give:", True, PALETTE["mint"]), (x, y + 8))
    y = draw_resource_buttons(
        screen,
        RESOURCE_ICONS,
        resources,
        trade_state,
        mouse,
        x,
        y,
        width,
        row_h,
        gap,
        panel_ui,
        "give",
    )

    # ---- RECEIVE ----
    screen.blit(font.render("Receive:", True, PALETTE["mint"]), (x, y + 8))
    y = draw_resource_buttons(
        screen,
        RESOURCE_ICONS,
        resources,
        trade_state,
        mouse,
        x,
        y,
        width,
        row_h,
        gap,
        panel_ui,
        "receive",
    )

    # ---- ACTION BUTTONS ----
    draw_action_buttons(screen, font, panel_ui, trade_state, rect, y, mouse)

    return panel_ui, hovered_tooltip
