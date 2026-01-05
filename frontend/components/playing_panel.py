import streamlit as st
from services.api_client import roll_dice


def render_playing_panel(game_state):
    st.divider()
    st.subheader("🎮 Playing Phase")

    if st.button("🎲 Roll Dice"):
        roll_dice()
        st.rerun()
