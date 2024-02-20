import streamlit as st
from functions.utility import (
    get_data,
    set_data,
    get_card,
    get_card_owner,
    check_time_exceeded,
)
from icecream import ic


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    this_character = players[player_code]["character"]
    show_card_to_player = get_data("show_card_to_player", game_code=game_code)
    if show_card_to_player:
        show_card_to_character = show_card_to_player["show_card_to_character"]
        if this_character == show_card_to_character:
            help = """Cards in this section are only visible to the indicated player."""
            st.title("Show Card to Player", help=help)
            placeholder = st.empty()
            table_card_columns = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

            card_col = table_card_columns[0]
            with card_col:
                card_id = show_card_to_player["show_card"]
                card = get_card(card_id)
                card_owner = get_card_owner(card_id)
                placeholder.info(
                    f"{card_owner['character']} is showing this card to {show_card_to_player['show_card_to_character']}"
                )
                st.image(
                    f"static/card_images/{card['image']}.png",
                    caption=f"{card['name']} ({card_owner['character']})",
                )

                viewing_time = 30_000
                is_time_exceeded = check_time_exceeded(viewing_time)

                if is_time_exceeded:
                    set_data("show_card_to_player", data=None, game_code=game_code)
