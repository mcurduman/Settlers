import pytest
from unittest.mock import patch, Mock


@patch("pygame.image.load")
@patch("pygame.transform.smoothscale", side_effect=lambda img, size: img)
def test_load_resource_icons(mock_smooth, mock_load):
    from client.render.panel import panel_assets

    mock_load.return_value.convert_alpha.return_value = Mock()
    icons = panel_assets.load_resource_icons()
    assert isinstance(icons, dict)
    assert "wood" in icons


@patch(
    "client.render.panel.panel_assets.load_resource_icons",
    return_value={"wood": Mock()},
)
def test_get_resource_icons(mock_load):
    from client.render.panel import panel_assets

    # Reset cache
    panel_assets.RESOURCE_ICONS = None
    icons = panel_assets.get_resource_icons()
    assert "wood" in icons
