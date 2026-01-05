import streamlit as st
import math
from services.api_client import place_settlement, place_road

# -------------------------------------------------
# Styles
# -------------------------------------------------
RESOURCE_STYLE = {
    "forest": ("#2E7D32", "🌲"),
    "clay": ("#BF360C", "🧱"),
    "wheat": ("#F9A825", "🌾"),
    "sheep": ("#7CB342", "🐑"),
    "desert": ("#E0C097", "🌵🐪🌵"),
}

HEX_SIZE = 100


# -------------------------------------------------
# Geometry helpers (MUST match backend math)
# -------------------------------------------------
def axial_to_pixel(q, r):
    x = HEX_SIZE * math.sqrt(3) * (q + r / 2)
    y = HEX_SIZE * 1.5 * r
    return x, y


def hex_points(cx, cy, size):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = cx + size * math.cos(angle)
        y = cy + size * math.sin(angle)
        points.append(f"{x},{y}")
    return " ".join(points)


def hex_corners(cx, cy, size):
    corners = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = cx + size * math.cos(angle)
        y = cy + size * math.sin(angle)
        corners.append((round(x, 2), round(y, 2)))
    return corners


# -------------------------------------------------
# Board rendering
# -------------------------------------------------
def render_board(game_state):
    tiles = game_state["board"]["tiles"]  # List of {q,r,resource,number}

    nodes = game_state["board"]["nodes"]  # (x,y) -> owner or None
    edges = game_state["board"]["edges"]  # ((x1,y1),(x2,y2)) -> owner or None

    from components.board_render import render_board_svg

    render_board_svg(tiles, edges, nodes)
