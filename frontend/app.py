import streamlit as st

# -------------------------------------------------
# App configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Mini Settlers",
    page_icon="🧱",
    layout="centered",
)

# -------------------------------------------------
# Session state initialization
# -------------------------------------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "game" not in st.session_state:
    st.session_state.game = None

# -------------------------------------------------
# Welcome / Home
# -------------------------------------------------
st.title("🧱 Mini Settlers")

st.markdown(
    """
    Welcome to **Mini Settlers**, a simplified version of *Settlers of Catan*.

    **How to play:**
    1. Go to **Start Game** and choose the AI difficulty.
    2. Start the game.
    3. View the board and play your turns.
    """
)

st.info("Use the sidebar to navigate between pages.")
