from client.render.board import board_constants


def test_hex_size_and_node_radius():
    assert board_constants.HEX_SIZE > 0
    assert board_constants.NODE_RADIUS > 0
