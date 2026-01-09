from client.render.panel import trade_panel


def test_get_button_state_give():
    resources = {"wood": 3}
    trade_state = {"give": "wood", "receive": "brick"}
    enabled, selected, is_same = trade_panel.get_button_state(
        "give", resources, trade_state, "wood"
    )
    assert enabled and selected and not is_same


def test_get_button_state_receive():
    resources = {"wood": 3}
    trade_state = {"give": "wood", "receive": "brick"}
    enabled, selected, is_same = trade_panel.get_button_state(
        "receive", resources, trade_state, "brick"
    )
    assert enabled and selected and not is_same


def test_get_give_button_colors():
    c = trade_panel.get_give_button_colors(True, True, True)
    assert isinstance(c, tuple)
    c = trade_panel.get_give_button_colors(False, False, False)
    assert isinstance(c, tuple)


def test_get_receive_button_colors():
    c = trade_panel.get_receive_button_colors(True, True, True)
    assert isinstance(c, tuple)
    c = trade_panel.get_receive_button_colors(False, False, False)
    assert isinstance(c, tuple)


def test_get_button_colors():
    c = trade_panel.get_button_colors("give", True, True, False, True)
    assert isinstance(c, tuple)
