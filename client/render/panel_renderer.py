import pygame
from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH
from client.assets.theme.resource_colors import RESOURCE_COLORS
from engine.game.rules.cost import COSTS
from client.input.helpers import can_trade_3_1, has_resources
from client.render.tooltip import draw_tooltip


STATE_HELPER = {
    "SetupRollState": "Roll the dice to start. Reroll if ties occur.",
    "SetupPlaceSettlementState": "Place a settlement on a valid node.",
    "SetupPlaceRoadState": "Place a road adjacent to your settlement.",
    "PlayingRollState": "Roll the dice to gather resources.",
    "PlayingMainState": "Build, trade, and strategize to win!",
    "PlayingPlaceRoadState": "Place a road on a valid edge.",
    "PlayingPlaceSettlementState": "Place a settlement on a valid node.",
    "PlayingTradeWithBankState": "Trade resources with the bank.",
}

TRADE_RESOURCES = ["sheep", "wheat", "brick", "wood"]


def load_resource_icons():
    icons = {}
    for res in [
        "sheep",
        "wheat",
        "brick",
        "wood",
        "trophy",
        "longest_road",
        "road",
        "settlement",
    ]:
        img = pygame.image.load(f"client/assets/resources/{res}.png").convert_alpha()
        icons[res] = pygame.transform.smoothscale(img, (32, 32))
    return icons


RESOURCE_ICONS = None


def is_distance_rule_violated(board, pos):
    for edge in board["edges"]:
        if edge["a"] == pos:
            other = edge["b"]
        elif edge["b"] == pos:
            other = edge["a"]
        else:
            continue

        for n in board["nodes"]:
            if n["position"] == other and n["owner"] is not None:
                return True
    return False


def is_connected_to_player_road(board, pos, player_name):
    for edge in board["edges"]:
        if edge["owner"] == player_name and (edge["a"] == pos or edge["b"] == pos):
            return True
    return False


def has_valid_settlement_spot(board, player_name):
    for node in board["nodes"]:
        if node["owner"] is not None:
            continue

        pos = node["position"]

        if is_distance_rule_violated(board, pos):
            continue

        if is_connected_to_player_road(board, pos, player_name):
            return True

    return False


def draw_roll_button(screen, rect, enabled):
    mouse = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse)

    bg = PALETTE["mint"] if enabled else PALETTE["blue_dark"]
    border = PALETTE["sand"] if hovered and enabled else PALETTE["blue"]

    pygame.draw.rect(screen, bg, rect, border_radius=10)
    pygame.draw.rect(screen, border, rect, 2, border_radius=10)

    font = pygame.font.Font(FONTS_PATH["bold"], 16)
    label = font.render("ROLL", True, PALETTE["bg_dark"])
    screen.blit(label, label.get_rect(center=rect.center))

    if hovered and enabled:
        draw_tooltip(screen, "Roll the dice to continue", mouse)


def draw_panel(screen, state, rect, trade_state):
    global RESOURCE_ICONS
    if RESOURCE_ICONS is None:
        RESOURCE_ICONS = load_resource_icons()

    pygame.draw.rect(screen, PALETTE["bg_dark"], rect)

    panel_ui = {
        "roll_button": None,
        "place_settlement_button": None,
        "place_road_button": None,
        "trade_with_bank_button": None,
        "end_turn_button": None,
    }

    x = rect.x + 16
    y = rect.y + 16
    width = rect.width - 32

    font_title = pygame.font.Font(FONTS_PATH["bold"], 28)
    font = pygame.font.Font(FONTS_PATH["bold"], 15)

    y = _draw_panel_phase_title_and_helper(screen, state, x, y, font_title, font)
    y, panel_ui, hovered_tooltip = _draw_panel_player_cards(
        screen, state, x, y, width, font_title, panel_ui, None
    )

    if state["state"] == "PlayingMainState":
        hovered_tooltip = _draw_panel_action_buttons(
            screen, state, x, y, width, panel_ui, hovered_tooltip
        )

    if state["state"] == "PlayingTradeWithBankState":
        trade_panel_ui, hovered_tooltip = draw_trade_with_bank_panel(
            screen, state, rect, trade_state, hovered_tooltip
        )

        if hovered_tooltip:
            text, pos = hovered_tooltip
            draw_tooltip(screen, text, pos)
        return panel_ui, trade_panel_ui

    if state["state"] in ("PlayingPlaceRoadState", "PlayingPlaceSettlementState"):
        panel_ui["cancel_placement_button"] = _draw_cancel_button(screen, rect)

    if hovered_tooltip:
        text, pos = hovered_tooltip
        draw_tooltip(screen, text, pos)

    return panel_ui, None


def _draw_panel_phase_title_and_helper(screen, state, x, y, font_title, font):
    PHASE_NAMES = {
        "SetupRollState": "Roll for Order",
        "SetupPlaceSettlementState": "Place Settlement",
        "SetupPlaceRoadState": "Place Road",
        "PlayingRollState": "Roll Dice",
        "PlayingMainState": "Your Turn",
        "PlayingPlaceRoadState": "Place Valid Road",
        "PlayingPlaceSettlementState": "Place Valid Settlement",
        "PlayingTradeWithBankState": "Trade with Bank",
    }
    phase = state["state"]
    screen.blit(
        font_title.render(PHASE_NAMES.get(phase, phase), True, PALETTE["sand"]),
        (x, y),
    )
    y += 35

    helper = STATE_HELPER.get(phase)
    if helper:
        screen.blit(font.render(helper, True, PALETTE["mint"]), (x, y))
        y += 34

    if state.get("error"):
        screen.blit(font.render(state["error"], True, PALETTE["red"]), (x, y))
        y += 28
    return y


def _draw_panel_player_cards(
    screen, state, x, y, width, font_title, panel_ui, hovered_tooltip=None
):
    hovered_tooltip = None
    for player in state["players"]:
        if (
            state["state"] == "PlayingTradeWithBankState"
            and str(player["name"].lower()) != "human"
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
            font_title,
            hovered_tooltip,
        )
        if roll_btn:
            panel_ui["roll_button"] = roll_btn
        if player_tooltip:
            hovered_tooltip = player_tooltip
        y += 12
    return y, panel_ui, hovered_tooltip


def _draw_panel_action_buttons(
    screen, state, x, y, width, panel_ui, hovered_tooltip=None
):
    current_player = next(
        p for p in state["players"] if p["name"] == state["current_player"]
    )

    hovered_tooltip_result = hovered_tooltip

    if not current_player["is_ai"]:
        resources = current_player["resources"]

        can_build_settlement = has_resources(
            resources, COSTS["settlement"]
        ) and has_valid_settlement_spot(state["board"], current_player["name"])

        can_build_road = has_resources(resources, COSTS["road"])
        can_trade = can_trade_3_1(resources)

        btn_defs = []

        if state["state"] == "PlayingPlaceSettlementState":
            btn_defs.append(
                ("Cancel", "cancel_placement_button", True, "Cancel placing settlement")
            )
        elif state["state"] == "PlayingPlaceRoadState":
            btn_defs.append(
                ("Cancel", "cancel_placement_button", True, "Cancel placing road")
            )
        else:
            btn_defs.extend(
                [
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
            )

        btn_w = (width - 16) // 2
        btn_h = 38
        gap = 16
        start_y = y + 10
        mouse = pygame.mouse.get_pos()

        for i, (label, key, enabled, tooltip) in enumerate(btn_defs):
            col = i % 2
            row = i // 2

            btn_x = x + col * (btn_w + gap)
            btn_y = start_y + row * (btn_h + gap)
            rect_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            hovered = rect_btn.collidepoint(mouse)

            if not enabled:
                bg = PALETTE["bg_dark"]
                border = PALETTE["blue"]
                txt_color = PALETTE["blue"]
            else:
                if key == "end_turn_button":
                    bg = PALETTE["sand"] if hovered else PALETTE["yellow"]
                    border = PALETTE["orange_dark"] if hovered else PALETTE["orange"]
                    txt_color = PALETTE["bg_dark"]
                elif key == "cancel_placement_button":
                    bg = PALETTE["orange_dark"] if hovered else PALETTE["orange"]
                    border = PALETTE["sand"] if hovered else PALETTE["orange_dark"]
                    txt_color = PALETTE["bg_dark"]
                else:
                    bg = PALETTE["mint"] if hovered else PALETTE["blue_dark"]
                    border = PALETTE["sand"] if hovered else PALETTE["blue"]
                    txt_color = PALETTE["bg_dark"]

            pygame.draw.rect(screen, bg, rect_btn, border_radius=10)
            pygame.draw.rect(screen, border, rect_btn, 2, border_radius=10)

            btn_font = pygame.font.Font(FONTS_PATH["bold"], 14)
            txt = btn_font.render(label, True, txt_color)
            screen.blit(txt, txt.get_rect(center=rect_btn.center))

            if enabled:
                panel_ui[key] = rect_btn
            elif hovered:
                hovered_tooltip_result = (tooltip, mouse)

    return hovered_tooltip_result


def draw_player_card(
    screen,
    state,
    player,
    current_player,
    x,
    y,
    width,
    font_title,
    hovered_tooltip=None,
):
    is_current = player["name"] == current_player
    is_human = player["name"].lower() == "human"

    bg = PALETTE["blue_dark"] if is_current else PALETTE["bg_dark"]
    border = PALETTE["mint"] if is_current else PALETTE["blue"]

    card_height = 200
    card_rect = pygame.Rect(x, y, width, card_height)

    pygame.draw.rect(screen, bg, card_rect, border_radius=12)
    pygame.draw.rect(screen, border, card_rect, 2, border_radius=12)

    name_y = y + 14
    cursor_x = x + 12

    player_color = PALETTE[str(player["name"]).lower()]
    circle_center = (cursor_x + 6, name_y + 18)
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        circle_center,
        8,
    )

    pygame.draw.circle(
        screen,
        player_color,
        circle_center,
        6,
    )
    cursor_x += 18

    is_longest_holder = state.get("longest_road_holder") == player["name"]

    player_tooltip = None

    if is_longest_holder:
        lr_icon = RESOURCE_ICONS["longest_road"]
        lr_rect = lr_icon.get_rect(topleft=(cursor_x, name_y))
        screen.blit(lr_icon, lr_rect)

        if lr_rect.collidepoint(pygame.mouse.get_pos()):
            player_tooltip = ("Longest Road\n+1 Victory Point", pygame.mouse.get_pos())
        cursor_x += lr_rect.width + 6

    name_surf = font_title.render(player["name"], True, border)
    screen.blit(name_surf, (cursor_x, name_y))

    y_icons = y + 50

    vp_icon = RESOURCE_ICONS["trophy"]
    lr_icon = RESOURCE_ICONS["longest_road"]
    settlement_icon = RESOURCE_ICONS["settlement"]
    road_icon = RESOURCE_ICONS["road"]

    mouse = pygame.mouse.get_pos()
    hovered_tooltip = None

    # Victory Points icon
    vp_rect = vp_icon.get_rect(topleft=(x + 12, y_icons))
    screen.blit(vp_icon, vp_rect)
    screen.blit(
        font_title.render(str(player["victory_points"]), True, PALETTE["yellow"]),
        (x + 52, y_icons + 2),
    )
    if vp_rect.collidepoint(mouse):
        hovered_tooltip = ("Victory Points", mouse)

    # Settlement icon
    settlement_rect = settlement_icon.get_rect(topleft=(x + width // 2 - 54, y_icons))
    screen.blit(settlement_icon, settlement_rect)
    screen.blit(
        font_title.render(
            str(len(player.get("settlements", []))), True, PALETTE["mint"]
        ),
        (x + width // 2 - 10, y_icons + 2),
    )
    if settlement_rect.collidepoint(mouse):
        hovered_tooltip = ("Settlements", mouse)

    # Road icon
    road_rect = road_icon.get_rect(topleft=(x + width // 2 + 24, y_icons))
    screen.blit(road_icon, road_rect)
    screen.blit(
        font_title.render(str(len(player.get("roads", []))), True, PALETTE["mint"]),
        (x + width // 2 + 62, y_icons + 2),
    )
    if road_rect.collidepoint(mouse):
        hovered_tooltip = ("Roads", mouse)

    # Longest Road icon
    lr_rect = lr_icon.get_rect(topleft=(x + width - 70, y_icons))
    screen.blit(lr_icon, lr_rect)
    screen.blit(
        font_title.render(str(player["longest_road"]), True, PALETTE["yellow"]),
        (x + width - 28, y_icons + 2),
    )
    if lr_rect.collidepoint(mouse):
        hovered_tooltip = ("Longest Road Length", mouse)

    ry = y_icons + 44
    rx = x + 12

    if is_human:
        for res in ["sheep", "wheat", "brick", "wood"]:
            val = player["resources"].get(res, 0)
            res_rect = RESOURCE_ICONS[res].get_rect(topleft=(rx, ry))
            screen.blit(RESOURCE_ICONS[res], res_rect)
            screen.blit(
                font_title.render(str(val), True, RESOURCE_COLORS[res]),
                (rx + 30, ry),
            )
            if res_rect.collidepoint(mouse):
                hovered_tooltip = (f"{res.capitalize()}: {val}", mouse)
            rx += 62
    else:
        for res in ["sheep", "wheat", "brick", "wood"]:
            res_rect = RESOURCE_ICONS[res].get_rect(topleft=(rx, ry))
            screen.blit(RESOURCE_ICONS[res], res_rect)
            if res_rect.collidepoint(mouse):
                hovered_tooltip = (f"{res.capitalize()}", mouse)
            rx += 34
        total = sum(player["resources"].values())
        screen.blit(
            font_title.render(str(total), True, PALETTE["mint"]),
            (rx + 6, ry),
        )

    # Draw the tooltip at the end, above all icons/text
    if hovered_tooltip:
        draw_tooltip(screen, hovered_tooltip[0], hovered_tooltip[1])

    roll = player.get("last_dice_roll", 0)
    dice_rect = pygame.Rect(x + width - 60, y + 140, 54, 54)

    try:
        dice_img = pygame.image.load(
            f"client/assets/dice/dice_{roll}.png"
        ).convert_alpha()
        dice_img = pygame.transform.smoothscale(dice_img, (40, 40))
        screen.blit(dice_img, dice_img.get_rect(center=dice_rect.center))
    except Exception:
        pass

    roll_button_rect = None
    if is_current and state["state"] in {"SetupRollState", "PlayingRollState"}:
        roll_button_rect = pygame.Rect(
            dice_rect.x - 70,
            dice_rect.y + 10,
            60,
            32,
        )
        draw_roll_button(screen, roll_button_rect, enabled=True)

    return y + card_height, roll_button_rect, player_tooltip


def draw_trade_with_bank_panel(screen, state, rect, trade_state, hovered_tooltip=None):
    # Accept hovered_tooltip as argument and propagate
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

    hovered_tooltip = None

    y = _draw_trade_panel_title(screen, font_title, x, y, row_h)
    y, panel_ui["trade_give"] = _draw_trade_panel_give(
        screen, font, x, y, width, resources, trade_state, mouse, gap, row_h
    )
    y, panel_ui["trade_receive"] = _draw_trade_panel_receive(
        screen, font, x, y, width, trade_state, mouse, gap, row_h
    )
    panel_ui = _draw_trade_panel_action_buttons(
        screen, font, rect, y, trade_state, panel_ui
    )

    # Return hovered_tooltip for consistency with tooltip-on-top logic
    return panel_ui, hovered_tooltip


def _draw_trade_panel_title(screen, font_title, x, y, row_h):
    screen.blit(
        font_title.render("Trade with Bank (3:1)", True, PALETTE["sand"]),
        (x, y),
    )
    return y + row_h


def _draw_trade_panel_give(
    screen, font, x, y, width, resources, trade_state, mouse, gap, row_h
):
    trade_give_ui = {}
    screen.blit(font.render("Give:", True, PALETTE["mint"]), (x, y + 8))
    btn_w = (width - 80) // 4
    bx = x + 60

    for res in ["sheep", "wheat", "brick", "wood"]:
        enabled = resources.get(res, 0) >= 3
        selected = trade_state["give"] == res

        rect_btn = pygame.Rect(bx, y, btn_w, row_h)
        hovered = rect_btn.collidepoint(mouse)

        if not enabled:
            bg = PALETTE["bg_dark"]
            border = PALETTE["blue"]
            alpha = 80
        else:
            bg = PALETTE["orange"] if selected else PALETTE["mint"]
            border = PALETTE["sand"] if hovered else PALETTE["blue"]
            alpha = 255

        pygame.draw.rect(screen, bg, rect_btn, border_radius=8)
        pygame.draw.rect(screen, border, rect_btn, 2, border_radius=8)

        icon = RESOURCE_ICONS[res].copy()
        icon.set_alpha(alpha)
        screen.blit(icon, icon.get_rect(center=rect_btn.center))

        if enabled:
            trade_give_ui[res] = rect_btn
        if hovered:
            if not enabled:
                draw_tooltip(screen, f"Need at least 3 {res} to trade", mouse)
            else:
                draw_tooltip(screen, f"Give 3 {res}", mouse)

        bx += btn_w + gap

    return y + row_h + gap, trade_give_ui


def _draw_trade_panel_receive(
    screen, font, x, y, width, trade_state, mouse, gap, row_h
):
    trade_receive_ui = {}
    screen.blit(font.render("Receive:", True, PALETTE["mint"]), (x, y + 8))
    btn_w = (width - 80) // 4
    bx = x + 60

    for res in ["sheep", "wheat", "brick", "wood"]:
        is_same_as_give = trade_state["give"] == res
        selected = trade_state["receive"] == res

        rect_btn = pygame.Rect(bx, y, btn_w, row_h)
        hovered = rect_btn.collidepoint(mouse)

        if is_same_as_give:
            bg = PALETTE["bg_dark"]
            border = PALETTE["blue"]
            alpha = 80
        else:
            bg = PALETTE["orange"] if selected else PALETTE["blue_dark"]
            border = PALETTE["sand"] if hovered else PALETTE["blue"]
            alpha = 255

        pygame.draw.rect(screen, bg, rect_btn, border_radius=8)
        pygame.draw.rect(screen, border, rect_btn, 2, border_radius=8)

        icon = RESOURCE_ICONS[res].copy()
        icon.set_alpha(alpha)
        screen.blit(icon, icon.get_rect(center=rect_btn.center))

        if not is_same_as_give:
            trade_receive_ui[res] = rect_btn
        if hovered:
            if is_same_as_give:
                draw_tooltip(screen, "Cannot receive same resource as you give", mouse)
            else:
                draw_tooltip(screen, f"Receive 1 {res}", mouse)

        bx += btn_w + gap

    return y + row_h + gap * 2, trade_receive_ui


def _draw_trade_panel_action_buttons(screen, font, rect, y, trade_state, panel_ui):
    confirm_enabled = (
        trade_state["give"] is not None
        and trade_state["receive"] is not None
        and trade_state["give"] != trade_state["receive"]
    )

    btn_w_action = 140
    btn_h_action = 40
    cx = rect.centerx - btn_w_action - 10
    rx = rect.centerx + 10

    confirm_rect = pygame.Rect(cx, y, btn_w_action, btn_h_action)
    cancel_rect = pygame.Rect(rx, y, btn_w_action, btn_h_action)
    mouse = pygame.mouse.get_pos()

    # CONFIRM (distinct color from CANCEL)
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
        if confirm_enabled:
            draw_tooltip(screen, "Confirm trade", mouse)
        else:
            draw_tooltip(screen, "Select resources to trade first", mouse)

    # CANCEL (make visually consistent with other cancel buttons)
    cancel_bg = PALETTE["orange"]
    cancel_border = (
        PALETTE["sand"] if cancel_rect.collidepoint(mouse) else PALETTE["orange_dark"]
    )
    pygame.draw.rect(screen, cancel_bg, cancel_rect, border_radius=12)
    pygame.draw.rect(screen, cancel_border, cancel_rect, 2, border_radius=12)

    screen.blit(
        font.render("CANCEL", True, PALETTE["bg_dark"]),
        font.render("CANCEL", True, PALETTE["bg_dark"]).get_rect(
            center=cancel_rect.center
        ),
    )

    panel_ui["cancel_trade"] = cancel_rect
    if cancel_rect.collidepoint(mouse):
        draw_tooltip(screen, "Cancel trade", mouse)

    return panel_ui


def _draw_cancel_button(screen, rect):
    btn_w = rect.width - 32
    btn_h = 42
    x = rect.x + 16
    y = rect.y + rect.height - btn_h - 80

    rect_btn = pygame.Rect(x, y, btn_w, btn_h)
    mouse = pygame.mouse.get_pos()
    hovered = rect_btn.collidepoint(mouse)

    # Make cancel button orange for uniformity
    bg = PALETTE["orange"]
    border = PALETTE["sand"] if hovered else PALETTE["orange_dark"]

    pygame.draw.rect(screen, bg, rect_btn, border_radius=12)
    pygame.draw.rect(screen, border, rect_btn, 2, border_radius=12)

    font = pygame.font.Font(FONTS_PATH["bold"], 16)
    txt = font.render("CANCEL", True, PALETTE["bg_dark"])
    screen.blit(txt, txt.get_rect(center=rect_btn.center))

    if hovered:
        draw_tooltip(screen, "Cancel placement", mouse)

    return rect_btn
