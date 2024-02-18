import streamlit as st
from functions.utility import (
    get_data,
    set_data,
    get_card,
    get_card_owner,
)
from icecream import ic


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    this_character = players[player_code]["character"]
    riddle_power_play = get_data("riddle_power_play", game_code=game_code)
    if riddle_power_play:
        riddler = riddle_power_play["riddler"]
        card_owner = riddle_power_play["card_owner"]
        is_riddler = this_character == riddler
        is_owner = this_character == card_owner
        if is_riddler or is_owner:
            help = """Cards in this section are only visible to the indicated player."""
            st.title("Riddle Area", help=help)
            placeholder = st.empty()
            table_card_columns = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

            card_col = table_card_columns[0]
            with card_col:
                card_id = riddle_power_play["riddle_card"]
                card = get_card(card_id)

                # card_owner = get_card_owner(card_id)
                placeholder.info(f"{riddler} is riddling {card_owner}'s card.")
                st.image(
                    f"static/card_images/{card['image']}.png",
                    caption=f"{card['name']} ({card_owner})",
                )
                # set_data("riddle_power_play", data=None, game_code=game_code)
