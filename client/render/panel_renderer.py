import pygame
from client.assets.theme.colors import PALETTE
from client.assets.theme.resource_colors import RESOURCE_COLORS


STATE_HELPER = {
    "SetupRollState": "Roll the dice to start.",
    "SetupPlaceSettlementState": "Place a settlement on a valid node.",
    "SetupPlaceRoadState": "Place a road adjacent to your settlement.",
    "PlayingState": "Choose an action for your turn.",
}


def load_resource_icons():
    icons = {}
    for res in [
        "sheep",
        "wheat",
        "clay",
        "forest",
        "trophy",
        "longest_road",
        "road",
        "settlement",
    ]:
        img = pygame.image.load(f"client/assets/resources/{res}.png").convert_alpha()
        icons[res] = pygame.transform.smoothscale(img, (32, 32))
    return icons


RESOURCE_ICONS = None


# ROLL BUTTON
def draw_roll_button(screen, rect, enabled):
    mouse = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse)

    bg = PALETTE["mint"] if enabled else PALETTE["blue_dark"]
    border = PALETTE["sand"] if hovered and enabled else PALETTE["blue"]

    pygame.draw.rect(screen, bg, rect, border_radius=10)
    pygame.draw.rect(screen, border, rect, 2, border_radius=10)

    font = pygame.font.Font("client/assets/fonts/Cinzel-Bold.ttf", 16)
    label = font.render("ROLL", True, PALETTE["bg_dark"])
    screen.blit(label, label.get_rect(center=rect.center))


# PANEL
def draw_panel(screen, state, rect):
    global RESOURCE_ICONS
    if RESOURCE_ICONS is None:
        RESOURCE_ICONS = load_resource_icons()

    pygame.draw.rect(screen, PALETTE["bg_dark"], rect)

    panel_ui = {
        "roll_button": None,
    }

    x = rect.x + 16
    y = rect.y + 16
    width = rect.width - 32

    font_title = pygame.font.Font("client/assets/fonts/Cinzel-Bold.ttf", 28)
    font = pygame.font.Font("client/assets/fonts/Cinzel-Bold.ttf", 15)

    PHASE_NAMES = {
        "SetupRollState": "Roll for Order",
        "SetupPlaceSettlementState": "Place Settlement",
        "SetupPlaceRoadState": "Place Road",
        "PlayingState": "Main Turn",
    }

    phase = state["state"]
    phase_pretty = PHASE_NAMES.get(phase, phase)

    screen.blit(
        font_title.render(phase_pretty, True, PALETTE["sand"]),
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

    for player in state["players"]:
        y, roll_btn = draw_player_card(
            screen,
            state,
            player,
            state["current_player"],
            x,
            y,
            width,
            font,
            font_title,
        )

        if roll_btn:
            panel_ui["roll_button"] = roll_btn

        y += 12

    return panel_ui


# PLAYER CARD
def draw_player_card(
    screen,
    state,
    player,
    current_player,
    x,
    y,
    width,
    font,
    font_title,
):
    is_current = player["name"] == current_player
    is_human = player["name"].lower() == "human"

    bg = PALETTE["blue_dark"] if is_current else PALETTE["bg_dark"]
    border = PALETTE["mint"] if is_current else PALETTE["blue"]

    card_height = 200
    card_rect = pygame.Rect(x, y, width, card_height)

    pygame.draw.rect(screen, bg, card_rect, border_radius=12)
    pygame.draw.rect(screen, border, card_rect, 2, border_radius=12)

    screen.blit(
        font_title.render(player["name"], True, border),
        (x + 12, y + 10),
    )

    y_icons = y + 50

    vp_icon = RESOURCE_ICONS["trophy"]
    lr_icon = RESOURCE_ICONS["longest_road"]
    settlement_icon = RESOURCE_ICONS["settlement"]
    road_icon = RESOURCE_ICONS["road"]

    screen.blit(vp_icon, (x + 12, y_icons))
    screen.blit(
        font_title.render(str(player["victory_points"]), True, PALETTE["yellow"]),
        (x + 52, y_icons + 2),
    )

    screen.blit(settlement_icon, (x + width // 2 - 54, y_icons))
    screen.blit(
        font_title.render(
            str(len(player.get("settlements", []))), True, PALETTE["mint"]
        ),
        (x + width // 2 - 10, y_icons + 2),
    )

    screen.blit(road_icon, (x + width // 2 + 24, y_icons))
    screen.blit(
        font_title.render(str(len(player.get("roads", []))), True, PALETTE["mint"]),
        (x + width // 2 + 62, y_icons + 2),
    )

    screen.blit(lr_icon, (x + width - 70, y_icons))
    screen.blit(
        font_title.render(str(player["longest_road"]), True, PALETTE["yellow"]),
        (x + width - 28, y_icons + 2),
    )

    # resources
    ry = y_icons + 44
    rx = x + 12

    if is_human:
        for res in ["sheep", "wheat", "clay", "forest"]:
            val = player["resources"].get(res, 0)
            screen.blit(RESOURCE_ICONS[res], (rx, ry))
            screen.blit(
                font_title.render(str(val), True, RESOURCE_COLORS[res]),
                (rx + 30, ry),
            )
            rx += 62
    else:
        for res in ["sheep", "wheat", "clay", "forest"]:
            screen.blit(RESOURCE_ICONS[res], (rx, ry))
            rx += 34
        total = sum(player["resources"].values())
        screen.blit(
            font_title.render(str(total), True, PALETTE["mint"]),
            (rx + 6, ry),
        )

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
    if is_current and state["state"] in {"SetupRollState", "PlayingState"}:
        roll_button_rect = pygame.Rect(
            dice_rect.x - 70,
            dice_rect.y + 10,
            60,
            32,
        )
        draw_roll_button(screen, roll_button_rect, enabled=True)

    return y + card_height, roll_button_rect
