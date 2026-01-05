import streamlit as st
from services.api_client import start_game


def render_main_screen():
    st.markdown(
        """
        <div style="text-align:center; margin-top:40px;">
            <h1 style="font-size:48px;">🏰 Mini Settlers</h1>
            <p style="font-size:20px; color:#9ca3af;">
                Choose your difficulty
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # ----------------------------
    # EASY
    # ----------------------------
    with col1:
        if st.button("🟢 EASY", use_container_width=True):
            start_game("easy")
            st.session_state.screen = "game"
            st.rerun()

        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #14532d, #166534);
                border-radius:16px;
                padding:24px;
                text-align:center;
                margin-top:-60px;
                pointer-events:none;
            ">
                <div style="font-size:28px; font-weight:bold; color:#bbf7d0;">
                    Beginner Friendly
                </div>
                <div style="margin-top:10px; color:#dcfce7;">
                    🧠 Slower AI<br>
                    🎁 More forgiving setup
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------
    # HARD
    # ----------------------------
    with col2:
        if st.button("🔴 HARD", use_container_width=True):
            start_game("hard")
            st.session_state.screen = "game"
            st.rerun()

        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #7f1d1d, #991b1b);
                border-radius:16px;
                padding:24px;
                text-align:center;
                margin-top:-60px;
                pointer-events:none;
            ">
                <div style="font-size:28px; font-weight:bold; color:#fecaca;">
                    Expert Mode
                </div>
                <div style="margin-top:10px; color:#fee2e2;">
                    🤖 Aggressive AI<br>
                    ⚔️ No mercy
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="text-align:center; margin-top:40px; color:#6b7280;">
            ⚠️ Difficulty cannot be changed once the game starts
        </div>
        """,
        unsafe_allow_html=True,
    )
