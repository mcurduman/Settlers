from unittest.mock import Mock


def test_draw_stats_row():
    from client.render.panel import player_card

    screen = Mock()
    font_title = Mock()
    resource_icons = {
        k: Mock(
            get_rect=Mock(
                return_value=Mock(
                    topleft=(0, 0),
                    colliderect=lambda x: False,
                    collidepoint=lambda x: False,
                )
            )
        )
        for k in ["trophy", "settlement", "road", "longest_road"]
    }
    player = {
        "victory_points": 2,
        "settlements": [1, 2],
        "roads": [1],
        "longest_road": 3,
    }
    x, width, y_icons, mouse = 0, 200, 0, (0, 0)
    tooltip = player_card.draw_stats_row(
        screen, font_title, resource_icons, player, x, width, y_icons, mouse
    )
    assert tooltip is None or isinstance(tooltip, tuple)
