import streamlit as st
from functions.utility import get_cards


def run():
    cards = get_cards()
    card_row_1 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    card_row_2 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    card_row_3 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    card_row_4 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    card_row_5 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    card_row_6 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    card_row_7 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    card_row_8 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    for card, card_column in zip(
        cards,
        card_row_1
        + card_row_2
        + card_row_3
        + card_row_4
        + card_row_5
        + card_row_6
        + card_row_7
        + card_row_8,
    ):
        include_in_draw_pile = card.get("include_in_draw_pile")
        if include_in_draw_pile == False:
            continue
        with card_column:
            st.image(
                f"static/card_images/{card['image']}.png",
                caption=f"{card['name']}",
            )
