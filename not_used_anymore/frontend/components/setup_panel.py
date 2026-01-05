import streamlit as st
from services.api_client import roll_dice
from components.players_row_hud import render_players_rows

STATE_HELPER = {
    "SetupRollState": {
        "title": "Setup – Roll Dice",
        "hint": "Roll the dice to determine the starting order.",
    },
    "SetupPlaceSettlementState": {
        "title": "Setup – Place Settlement",
        "hint": "Place a settlement on a valid node on the board.",
    },
    "SetupPlaceRoadState": {
        "title": "Setup – Place Road",
        "hint": "Place a road connected to your settlement.",
    },
}


def render_setup_panel(game_state):
    players = game_state.get("players", [])
    current_player = game_state.get("current_player")
    state = game_state.get("state")

    helper = STATE_HELPER.get(state, {"title": state, "hint": ""})

    # 🧠 STATE TITLE + HELPER
    st.markdown(f"### 🧠 {helper['title']}")
    if helper["hint"]:
        st.info(helper["hint"])

    # 👥 PLAYERS (row layout)
    if players:
        render_players_rows(players, current_player)

    st.divider()

    # 🎲 ACTION (only meaningful in roll state)
    if state == "SetupRollState":
        if st.button("🎲 Roll Dice", use_container_width=True):
            result = roll_dice()
            if "detail" in result:
                st.warning(result["detail"])
            else:
                st.rerun()
