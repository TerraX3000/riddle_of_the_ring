import streamlit as st
from functions.utility import get_data


def run():
    with st.container():
        st.markdown("# Players")
        characters = get_data("characters")
        players = get_data("players")
        for player in players:
            if player["character"] == st.session_state["player"]["character"]:
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
