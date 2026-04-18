import streamlit as st
from functions.utility import get_data
from icecream import ic


def run():
    query_params = st.query_params.to_dict()
    game_code = query_params.get("game")
    player_code = query_params.get("player")
    players = get_data("players", game_code=game_code)

    with st.container(border=True):
        st.title("Players")
        characters = get_data("characters")
        players = get_data("players", game_code=game_code)
        for player in players.values():
            if player["character"] == players[player_code]["character"]:
                player_name = "me"
            else:
                player_name = player["name"]
            color = characters[player["character"]]["color"]
            player_markdown_1 = f"### :{color}[{player['character']}]"
            player_markdown_2 = f"""##### :{color}[({player_name})]"""
            st.markdown(player_markdown_1)
            st.markdown(player_markdown_2)
            if player["current_turn"]:
                st.markdown(f"""##### :{color}[Current Turn]""")
