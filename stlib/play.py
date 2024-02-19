import streamlit as st
from streamlit_autorefresh import st_autorefresh
from sections import (
    game_chat_section,
    navbar,
    player_section,
    cards_section,
    action_section,
    board_section,
    activity_section,
    discard_section,
    battle_section,
    game_stats_section,
)
from functions.utility import (
    show_battle_section,
    initialize_game_data,
    get_shuffled_deck,
    get_data,
)

from streamlit_shortcuts import add_keyboard_shortcuts


def run():
    st.query_params.page = "play"
    query_params = st.query_params.to_dict()
    game_code = query_params.get("game")
    player_code = query_params.get("player")
    navbar.run()
    auto_refresh = st.toggle("Auto Refresh", value=True)
    if auto_refresh:
        st_autorefresh(interval=10000, limit=None, key="riddle")

    if not game_code or not player_code:
        st.error(
            "Game Code and Player Code are required to play.  Please start a new game or join an existing game."
        )
    else:
        style = """<style>h2,h3,h4,h5,h6 {text-align: center;}</style>"""
        st.markdown(style, unsafe_allow_html=True)
        add_keyboard_shortcuts(
            {
                "Alt+®": "Refresh Game (Alt+R)",
            }
        )
        col_top_left, col_top_right = st.columns([0.5, 0.5])

        game_chat_section.run(col_top_left)

        with col_top_right:
            game_stats_section.run()

        col_1, col_2, col_3 = st.columns([0.1, 0.5, 0.4])

        with col_1:
            player_section.run()

        with col_2:
            cards_section.run()

        with col_3:
            action_section.run()

        if show_battle_section():
            with st.container(border=True):
                st.markdown("# Battle")
                with st.container():
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        battle_section.run("attacker")
                    with col2:
                        battle_section.run("defender")

        col_4, col_5, col_6 = st.columns([1, 3, 1])

        with col_4:
            activity_section.run()

        with col_5:
            board_section.run()

        with col_6:
            discard_section.run()
