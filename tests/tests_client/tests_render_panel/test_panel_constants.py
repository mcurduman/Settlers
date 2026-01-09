def test_panel_constants_content():
    from client.render.panel import panel_constants

    assert "SetupRollState" in panel_constants.PHASE_NAMES
    assert "PlayingMainState" in panel_constants.STATE_HELPER
    assert "wood" in panel_constants.TRADE_RESOURCES
