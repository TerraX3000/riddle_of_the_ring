import streamlit as st
from icecream import ic


def run():
    query_params = st.query_params.to_dict()
    ic(query_params)
    nav_1, nav_2, nav_3, nav_4, spacer, nav_game_info, nav_player_info = st.columns(
        [1.5, 1.5, 1.5, 1.5, 3, 1.5, 1.5]
    )
    with nav_1:
        if st.button("Home", use_container_width=True):
            st.query_params.page = "index"
            st.rerun()

    with nav_2:
        if st.button("Game Info", use_container_width=True):
            st.query_params.page = "info"
            st.rerun()

    is_show_start_and_resume_buttons = False
    is_show_play_button = False
    is_show_exit_button = False
    page = query_params.get("page")

    if page == "play":
        is_show_start_and_resume_buttons = False
        is_show_exit_button = True
    elif "player" in query_params and "game" in query_params:
        is_show_start_and_resume_buttons = False
        is_show_play_button = True
        is_show_exit_button = True
    else:
        is_show_start_and_resume_buttons = True

    if is_show_start_and_resume_buttons:
        with nav_3:
            if st.button("Start or Join Game", use_container_width=True):
                st.query_params.page = "start_or_join_game"
                st.rerun()
        with nav_4:
            if st.button("Resume Game", use_container_width=True):
                st.query_params.page = "resume_game"
                st.rerun()
    elif is_show_play_button and is_show_exit_button:
        with nav_3:
            if st.button("Return to Game", use_container_width=True):
                st.query_params.page = "play"
                st.rerun()
        with nav_4:
            if st.button("Exit Game", use_container_width=True):
                st.query_params.page = "exit_game"
                st.rerun()
    elif is_show_exit_button:
        with nav_3:
            st.button("Return to Game", use_container_width=True, disabled=True)
        with nav_4:
            if st.button("Exit Game", use_container_width=True):
                st.query_params.page = "exit_game"
                st.rerun()
    elif is_show_play_button:
        with nav_3:
            if st.button("Return to Game", use_container_width=True):
                st.query_params.page = "play"
                st.rerun()

    if "player" in query_params and "game" in query_params:
        with nav_game_info:
            st.subheader(
                f"Game Code: {query_params['game']}",
                anchor=False,
            )
        with nav_player_info:
            st.subheader(
                f"Player Code: {query_params['player']}",
                anchor=False,
            )
