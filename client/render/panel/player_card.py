import pygame

from client.assets.theme.colors import PALETTE
from client.assets.theme.fonts import FONTS_PATH
from client.assets.theme.resource_colors import RESOURCE_COLORS
from client.render.tooltip import draw_tooltip
from .panel_assets import get_resource_icons
from .buttons import draw_roll_button


def draw_stats_row(
    screen, font_title, resource_icons, player, x, width, y_icons, mouse
):
    """
    Draws the stats row (victory points, settlements, roads, longest road) for a player card.
    Returns a tooltip if a stat is hovered.
    """
    hovered_tooltip = None

    def draw_stat(icon, value, pos_x, tooltip, color):
        nonlocal hovered_tooltip
        rect = icon.get_rect(topleft=(pos_x, y_icons))
        screen.blit(icon, rect)
        screen.blit(
            font_title.render(str(value), True, color),
            (pos_x + 40, y_icons + 2),
        )
        if rect.collidepoint(mouse):
            hovered_tooltip = (tooltip, mouse)

    draw_stat(
        resource_icons["trophy"],
        player["victory_points"],
        x + 12,
        "Victory Points",
        PALETTE["yellow"],
    )
    draw_stat(
        resource_icons["settlement"],
        len(player.get("settlements", [])),
        x + width // 2 - 54,
        "Settlements",
        PALETTE["mint"],
    )
    draw_stat(
        resource_icons["road"],
        len(player.get("roads", [])),
        x + width // 2 + 24,
        "Roads",
        PALETTE["mint"],
    )
    draw_stat(
        resource_icons["longest_road"],
        player["longest_road"],
        x + width - 70,
        "Longest Road Length",
        PALETTE["yellow"],
    )
    return hovered_tooltip


def draw_resources_row(
    screen,
    font_title,
    resource_icons,
    resource_colors,
    player,
    x,
    ry,
    is_human,
    mouse,
):
    """
    Draws the resources row for a player card, showing resource icons and counts.
    Returns a tooltip if a resource is hovered.
    """
    hovered_tooltip = None
    rx = x + 12
    if is_human:
        for res in ["sheep", "wheat", "brick", "wood"]:
            val = player["resources"].get(res, 0)
            res_rect = resource_icons[res].get_rect(topleft=(rx, ry))
            screen.blit(resource_icons[res], res_rect)
            screen.blit(
                font_title.render(str(val), True, resource_colors[res]),
                (rx + 30, ry),
            )
            if res_rect.collidepoint(mouse):
                hovered_tooltip = (f"{res.capitalize()}: {val}", mouse)
            rx += 62
    else:
        for res in ["sheep", "wheat", "brick", "wood"]:
            res_rect = resource_icons[res].get_rect(topleft=(rx, ry))
            screen.blit(resource_icons[res], res_rect)
            if res_rect.collidepoint(mouse):
                hovered_tooltip = (res.capitalize(), mouse)
            rx += 34
        total = sum(player["resources"].values())
        screen.blit(
            font_title.render(str(total), True, PALETTE["mint"]),
            (rx + 6, ry),
        )
    return hovered_tooltip


def draw_player_card(
    screen,
    state,
    player,
    current_player,
    x,
    y,
    width,
):
    """
    Draws a player card with name, stats, resources, dice, and roll button if needed.
    Returns new y, roll button rect, and player tooltip if hovered.
    """
    resource_icons = get_resource_icons()

    is_current = player["name"] == current_player
    is_human = str(player["name"]).lower() == "human"

    bg = PALETTE["blue_dark"] if is_current else PALETTE["bg_dark"]
    border = PALETTE["mint"] if is_current else PALETTE["blue"]

    card_height = 200
    card_rect = pygame.Rect(x, y, width, card_height)

    pygame.draw.rect(screen, bg, card_rect, border_radius=12)
    pygame.draw.rect(screen, border, card_rect, 2, border_radius=12)

    name_y = y + 14
    cursor_x = x + 12

    player_color = PALETTE[str(player["name"]).lower()]
    circle_center = (cursor_x + 6, name_y + 14)

    pygame.draw.circle(screen, (255, 255, 255), circle_center, 8)
    pygame.draw.circle(screen, player_color, circle_center, 6)
    cursor_x += 18

    is_longest_holder = state.get("longest_road_holder") == player["name"]
    player_tooltip = None
    mouse = pygame.mouse.get_pos()

    if is_longest_holder:
        lr_icon = resource_icons["longest_road"]
        lr_rect = lr_icon.get_rect(topleft=(cursor_x, name_y))
        screen.blit(lr_icon, lr_rect)

        if lr_rect.collidepoint(mouse):
            player_tooltip = ("Longest Road\n+1 Victory Point", mouse)
        cursor_x += lr_rect.width + 6

    font_title = pygame.font.Font(FONTS_PATH["bold"], 20)
    name_surf = font_title.render(player["name"], True, border)
    screen.blit(name_surf, (cursor_x, name_y))

    # --- ICONS ROW ---
    y_icons = y + 50

    hovered_tooltip = draw_stats_row(
        screen, font_title, resource_icons, player, x, width, y_icons, mouse
    )

    # --- RESOURCES ---
    ry = y_icons + 44
    hovered_tooltip_res = draw_resources_row(
        screen,
        font_title,
        resource_icons,
        RESOURCE_COLORS,
        player,
        x,
        ry,
        is_human,
        mouse,
    )
    if hovered_tooltip_res:
        hovered_tooltip = hovered_tooltip_res

    # --- DICE ---
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

    if hovered_tooltip:
        draw_tooltip(screen, hovered_tooltip[0], hovered_tooltip[1])

    return y + card_height, roll_button_rect, player_tooltip
