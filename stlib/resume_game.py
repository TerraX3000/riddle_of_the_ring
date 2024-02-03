import streamlit as st
from sections import navbar
from icecream import ic


def run():
    st.query_params.page = "resume_game"
    navbar.run()
    st.write("Resume game")
    code_column, unused = st.columns([2, 10])
    with code_column:
        game_code = st.text_input("Enter Game Code")
        player_code = st.text_input("Enter Player Code")

    if st.button("Resume Game"):
        if game_code and player_code:
            st.query_params.game = game_code
            st.query_params.player = player_code
            st.query_params.page = "play"
            st.rerun()
        elif any([game_code, player_code]):
            st.info("Both game code and player code are required")
