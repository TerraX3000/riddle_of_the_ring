import streamlit as st
from streamlit_sortables import sort_items
from functions.utility import (
    get_data,
    get_card,
    get_card_owner,
    discard_table_card,
    retain_table_card,
)
from collections import OrderedDict
from icecream import ic


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    help = """Place cards on the table when you use them for power plays or other purposes.  Cards on the table are visible to all players."""
    st.title("Table Cards", help=help)
    table_cards = get_data("table_cards", game_code=game_code)
    table_card_columns = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    for (
        card_id,
        card_col,
    ) in zip(table_cards, table_card_columns):
        with card_col:
            card = get_card(card_id)
            card_owner = get_card_owner(card_id)
            st.button(
                "Discard",
                key=f'table_discard_{card["id"]}',
                on_click=discard_table_card,
                kwargs={"card_id": card["id"]},
            )
            st.button(
                "Retain",
                key=f'table_retain_{card["id"]}',
                on_click=retain_table_card,
                kwargs={"card_id": card["id"]},
            )
            st.image(
                f"data/card_images/{card['image']}.png",
                caption=f"{card['name']} ({card_owner['character']})",
            )
