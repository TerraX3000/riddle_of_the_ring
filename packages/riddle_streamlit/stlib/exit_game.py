import streamlit as st
from sections import navbar
from icecream import ic
from functions import redis_functions
from functions.utility import get_data, set_data


def run():
    st.query_params.page = "exit_game"
    navbar.run()
    query_params = st.query_params.to_dict()
    game_code = query_params.get("game")
    st.write("Are you sure you want to exit the game?")
    if st.button("Yes - Delete All My Player Info"):
        st.query_params.clear()
        keys = [
            "players",
            "activities",
            "draw_pile",
            "discards",
            "characters",
            "battle",
            "points",
            "table_cards",
            "game",
            "show_card_to_player",
            "friendly_exchange",
            "riddle_power_play",
            "assistant_replies_index",
        ]
        for key in keys:
            redis_functions.delete_data(key, game_code=game_code)
        games = get_data("games")
        for game in games:
            if game_code == game.get("game_code"):
                games.remove(game)
                break
        set_data("games", games)

        st.session_state.clear()
        st.query_params.page = "index"
        st.rerun()
    if st.button("No - Take Me Back to My Game"):
        st.query_params.page = "play"
        st.rerun()
