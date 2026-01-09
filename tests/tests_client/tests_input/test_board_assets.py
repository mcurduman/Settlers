from unittest.mock import Mock
from client.render.board import board_assets


def test_load_tile_icons_caching(monkeypatch):
    board_assets._TILE_ICONS.clear()
    monkeypatch.setattr(board_assets, "pygame", Mock())
    # First call triggers loading
    board_assets._TILE_ICONS.clear()
    monkeypatch.setattr(board_assets, "HEX_SIZE", 10)
    monkeypatch.setattr(board_assets, "pygame", Mock())
    monkeypatch.setattr(board_assets, "_TILE_ICONS", {})
    monkeypatch.setattr(board_assets, "pygame", Mock())
    # Patch image loading and scaling
    fake_img = Mock()
    fake_img.get_rect.return_value = Mock()
    fake_img.convert_alpha.return_value = fake_img
    fake_img.set_alpha = Mock()
    fake_img.get_rect = Mock(return_value=Mock())
    fake_img.get_rect.return_value = Mock()
    fake_img.get_rect.return_value.center = (0, 0)
    fake_img.get_rect.return_value = Mock()
    fake_img.get_rect.return_value.center = (0, 0)
    fake_img.get_rect.return_value = Mock()
    fake_img.get_rect.return_value.center = (0, 0)
    fake_img.get_rect.return_value = Mock()
    fake_img.get_rect.return_value.center = (0, 0)
    fake_img.get_rect.return_value = Mock()
    fake_img.get_rect.return_value.center = (0, 0)
    monkeypatch.setattr(
        board_assets.pygame, "image", Mock(load=Mock(return_value=fake_img))
    )
    monkeypatch.setattr(
        board_assets.pygame, "transform", Mock(smoothscale=Mock(return_value=fake_img))
    )
