import streamlit as st
from icecream import ic


def run():
    query_params = st.query_params.to_dict()
    ic(query_params)
    nav_1, nav_2, nav_3, unused = st.columns([1.5, 1.5, 1.5, 8])
    with nav_1:
        if st.button("Home", use_container_width=True):
            st.query_params.page = "index"
            st.rerun()

    with nav_2:
        if st.button("Game Info", use_container_width=True):
            st.query_params.page = "info"
            st.rerun()

    try:
        is_show_start_button = False
        is_show_play_button = False
        page = query_params.get("page")
        if page == "play":
            is_show_start_button = False
        elif "player" in query_params and "game" in query_params:
            is_show_start_button = False
            is_show_play_button = True
        else:
            is_show_start_button = True
    except:
        is_show_start_button = True

    if is_show_start_button:
        with nav_3:
            if st.button("Start New Game", use_container_width=True):
                st.query_params.page = "start_new_game"
                st.rerun()
    elif is_show_play_button:
        with nav_3:
            if st.button("Return to Game", use_container_width=True):
                st.query_params.page = "play"
                st.rerun()
