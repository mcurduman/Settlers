def get_state(state_name: str):
    if state_name == "SetupPlaceSettlementState":
        from app.game.states.setup.setup_place_settlement_state import (
            SetupPlaceSettlementState,
        )

        return SetupPlaceSettlementState()

    if state_name == "SetupPlaceRoadState":
        from app.game.states.setup.setup_place_road_state import SetupPlaceRoadState

        return SetupPlaceRoadState()

    if state_name == "SetupRollState":
        from app.game.states.setup.setup_roll_state import SetupRollState

        return SetupRollState()

    if state_name == "PlayingState":
        from app.game.states.playing_state import PlayingState

        return PlayingState()
    raise ValueError(f"Unknown state: {state_name}")
