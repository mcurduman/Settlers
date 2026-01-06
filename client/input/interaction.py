import pygame
import math
from client.render.board_renderer import axial_to_screen, NODE_RADIUS
from client.render.coord import world_to_screen


def is_hovered(mouse_pos, screen_pos, radius=NODE_RADIUS):
    return math.dist(mouse_pos, screen_pos) <= radius


def handle_interaction(event, state, game, board_rect):
    current_state = state["state"]

    if current_state == "SetupPlaceSettlementState":
        handle_setup_place_settlement(event, state, game, board_rect)

    elif current_state == "SetupPlaceRoadState":
        handle_setup_place_road(event, state, game, board_rect)


def handle_setup_place_settlement(event, state, game, board_rect):
    mouse_pos = pygame.mouse.get_pos()
    hovered = None

    for node in state["board"]["nodes"]:
        if node["owner"] is not None:
            continue

        screen_pos = world_to_screen(node["position"], board_rect)

        if math.dist(mouse_pos, screen_pos) <= NODE_RADIUS + 6:
            hovered = node["position"]

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.place_settlement(node["position"])
                return None  # după click, nu mai highlight

    return hovered


def handle_setup_place_road(event, state, game, board_rect):
    mouse_pos = pygame.mouse.get_pos()
    hovered_edge = None

    for edge in state["board"]["edges"]:
        if edge["owner"] is not None:
            continue

        a = world_to_screen(edge["a"], board_rect)
        b = world_to_screen(edge["b"], board_rect)

        if point_near_segment(mouse_pos, a, b, tolerance=14):
            hovered_edge = edge

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.place_road(edge["a"], edge["b"])
                return None

    return hovered_edge

def point_near_segment(p, a, b, tolerance):
    px, py = p
    ax, ay = a
    bx, by = b

    # vector AB
    abx = bx - ax
    aby = by - ay

    # vector AP
    apx = px - ax
    apy = py - ay

    ab_len_sq = abx * abx + aby * aby
    if ab_len_sq == 0:
        # a == b
        return (apx * apx + apy * apy) <= tolerance * tolerance

    # proiecție scalară
    t = (apx * abx + apy * aby) / ab_len_sq
    t = max(0.0, min(1.0, t))

    # punctul cel mai apropiat
    cx = ax + t * abx
    cy = ay + t * aby

    dx = px - cx
    dy = py - cy

    return (dx * dx + dy * dy) <= tolerance * tolerance
