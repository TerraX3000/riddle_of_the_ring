import streamlit as st
from sections import navbar
from icecream import ic
from functions.utility import get_data


def run():
    st.query_params.page = "admin"
    navbar.run()
    query_params = st.query_params.to_dict()
    game_code = query_params.get("game")
    st.write("Admin")
    col_1, col_2, col_3, col_4 = st.columns([1, 1, 1, 1])

    with col_1:
        st.write("Session State")
        st.write(st.session_state)
        st.write("Game")
        st.write(get_data("game", game_code=game_code))
        st.write("Games")
        st.write(get_data("games"), game_code=game_code)
        st.write("Battle")
        st.write(get_data("battle", game_code=game_code))
        st.write("Table Cards")
        st.write(get_data("table_cards", game_code=game_code))
    with col_2:
        st.write("Players")
        st.write(get_data("players", game_code=game_code))
    with col_3:
        st.write("Activities")
        st.write(get_data("activities", game_code=game_code))
        st.write("Characters")
        st.write(get_data("characters"))
    with col_4:
        st.write("Draw Pile")
        st.write(get_data("draw_pile", game_code=game_code))
        st.write("Discards")
        st.write(get_data("discards", game_code=game_code))
