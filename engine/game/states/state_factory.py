def get_state(state_name: str):
    if state_name == "SetupPlaceSettlementState":
        from engine.game.states.setup.setup_place_settlement_state import (
            SetupPlaceSettlementState,
        )

        return SetupPlaceSettlementState()

    if state_name == "SetupPlaceRoadState":
        from engine.game.states.setup.setup_place_road_state import SetupPlaceRoadState

        return SetupPlaceRoadState()

    if state_name == "SetupRollState":
        from engine.game.states.setup.setup_roll_state import SetupRollState

        return SetupRollState()

    if state_name == "PlayingMainState":
        from engine.game.states.playing.playing_main_state import PlayingMainState

        return PlayingMainState()

    if state_name == "PlayingRollState":
        from engine.game.states.playing.playing_roll_state import PlayingRollState

        return PlayingRollState()
    raise ValueError(f"Unknown state: {state_name}")
