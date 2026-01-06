import math

HEX_SIZE = 100
SCALE = HEX_SIZE


def world_to_screen(pos, board_rect):
    """
    Convert engine world coords (float x,y) to screen pixels.
    """
    cx = board_rect.x + board_rect.width // 2
    cy = board_rect.y + board_rect.height // 2

    x, y = pos
    return int(cx + x * SCALE), int(cy + y * SCALE)


def axial_to_screen(q, r, board_rect):
    """
    Convert axial hex coords (q, r) to screen pixels.
    """
    cx = board_rect.x + board_rect.width // 2
    cy = board_rect.y + board_rect.height // 2

    x = SCALE * math.sqrt(3) * (q + r / 2)
    y = SCALE * 1.5 * r

    return int(cx + x), int(cy + y)
