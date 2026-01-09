from client.render.board import board_geometry
import math

def test_hex_corners_count():
    corners = board_geometry.hex_corners(0, 0, 10)
    assert len(corners) == 6

def test_hex_corners_shape():
    corners = board_geometry.hex_corners(0, 0, 10)
    for x, y in corners:
        assert isinstance(x, float)
        assert isinstance(y, float)
