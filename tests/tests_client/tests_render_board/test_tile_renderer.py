from unittest.mock import Mock

from client.render.board import tile_renderer


def test_draw_tile_and_tiles(monkeypatch):
    screen = Mock()
    tile = {"q": 0, "r": 0, "resource": "wood", "number": 8}
    board_rect = Mock()
    icons = {
        "wood": Mock(get_rect=Mock(return_value=Mock(center=(0, 0))), set_alpha=Mock())
    }
    monkeypatch.setattr(tile_renderer, "axial_to_screen", Mock(return_value=(0, 0)))
    monkeypatch.setattr(tile_renderer, "hex_corners", Mock(return_value=[(0, 0)] * 6))
    monkeypatch.setattr(
        tile_renderer,
        "pygame",
        Mock(
            draw=Mock(),
            font=Mock(
                Font=Mock(
                    return_value=Mock(
                        render=Mock(
                            return_value=Mock(
                                get_rect=Mock(return_value=Mock(center=(0, 0)))
                            )
                        )
                    )
                )
            ),
            PALETTE={"bg_dark": (0, 0, 0)},
        ),
    )
    monkeypatch.setattr(tile_renderer, "RESOURCE_COLORS", {"wood": (0, 0, 0)})
    monkeypatch.setattr(tile_renderer, "FONTS_PATH", {"extra_bold": ""})
    tile_renderer.draw_tile(screen, tile, board_rect, icons)
    tile_renderer.draw_tiles(screen, [tile], board_rect, icons)
