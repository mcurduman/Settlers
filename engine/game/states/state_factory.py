def get_state(state_name: str):
    if state_name == "SetupPlaceSettlementState":
        from engine.game.states.setup.setup_place_settlement_state import (
            SetupPlaceSettlementState,
        )

        return SetupPlaceSettlementState()

    elif state_name == "SetupPlaceRoadState":
        from engine.game.states.setup.setup_place_road_state import SetupPlaceRoadState

        return SetupPlaceRoadState()

    elif state_name == "SetupRollState":
        from engine.game.states.setup.setup_roll_state import SetupRollState

        return SetupRollState()

    elif state_name == "PlayingMainState":
        from engine.game.states.playing.playing_main_state import PlayingMainState

        return PlayingMainState()

    elif state_name == "PlayingRollState":
        from engine.game.states.playing.playing_roll_state import PlayingRollState

        return PlayingRollState()
    elif state_name == "PlayingPlaceRoadState":
        from engine.game.states.playing.playing_place_road_state import (
            PlayingPlaceRoadState,
        )

        return PlayingPlaceRoadState()
    elif state_name == "PlayingPlaceSettlementState":
        from engine.game.states.playing.playing_place_settlement_state import (
            PlayingPlaceSettlementState,
        )

        return PlayingPlaceSettlementState()

    elif state_name == "PlayingTradeWithBankState":
        from engine.game.states.playing.playing_trade_with_bank_state import (
            PlayingTradeWithBankState,
        )

        return PlayingTradeWithBankState()
    elif state_name == "FinishedState":
        from engine.game.states.finished.finished_state import FinishedState

        return FinishedState()
    raise ValueError(f"Unknown state: {state_name}")
