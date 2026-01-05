import streamlit as st
from components.board_view import render_board
from components.setup_panel import render_setup_panel
from components.start_screen import render_main_screen
from services.api_client import get_state

# -------------------------------------------------
# App configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Mini Settlers",
    page_icon="🧱",
    layout="wide",
)

# -------------------------------------------------
# INITIAL SYNC WITH BACKEND (RUNS ON REFRESH)
# -------------------------------------------------
if "screen" not in st.session_state:
    game_state = get_state()

    if isinstance(game_state, dict) and "detail" not in game_state:
        # ✅ Game already exists → go straight to game
        st.session_state.screen = "game"
    else:
        # ❌ No game → show main screen
        st.session_state.screen = "main"

# -------------------------------------------------
# MAIN SCREEN
# -------------------------------------------------
if st.session_state.screen == "main":
    render_main_screen()
    st.stop()

# -------------------------------------------------
# GAME SCREEN
# -------------------------------------------------
if st.session_state.screen == "game":
    game_state = get_state()

    # Game was reset / ended
    if isinstance(game_state, dict) and "detail" in game_state:
        if game_state["detail"] == "Game has not been started":
            st.session_state.screen = "main"
            st.rerun()
        else:
            st.error(game_state["detail"])
            st.stop()

    left, right = st.columns([2, 1], gap="medium")

    with left:
        render_board(game_state)

    with right:
        render_setup_panel(game_state)
