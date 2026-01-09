import math


def hex_corners(cx, cy, size):
    """
    Calculate the corner points of a hexagon.
    """
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        points.append((cx + size * math.cos(angle), cy + size * math.sin(angle)))
    return points
