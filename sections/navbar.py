import streamlit as st
from icecream import ic


def run():
    query_params = st.query_params.to_dict()
    nav_1, nav_2, nav_3, nav_4, nav_5, spacer, nav_game_info, nav_player_info = (
        st.columns([1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2])
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
            if st.button("Refresh Game", use_container_width=True):
                st.query_params.page = "play"
                st.rerun()
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
            help = "Share the Game Code with other players to join your game."
            st.subheader(
                f"_Game Code:_ &nbsp; :blue[{query_params['game']}]",
                anchor=False,
                help=help,
            )
        with nav_player_info:
            help = "Remember your *secret* Player Code to restore your player settings in this game (e.g., if you accidentally close your browser).  No one else can see your Player Code."
            st.subheader(
                f"_Player Code:_ &nbsp; :blue[{query_params['player']}]",
                anchor=False,
                help=help,
            )
    with nav_5:
        if st.button("Admin", use_container_width=True):
            st.query_params.page = "admin"
            st.rerun()
