import streamlit as st
from functions.utility import get_data, get_card


def run():
    st.markdown("# Discard Pile")
    game_code = st.query_params.game
    with st.container(height=1000):
        discard_pile = get_data("discards", game_code=game_code)
        for card_id in reversed(discard_pile):
            card = get_card(card_id)
            st.markdown(f"### {card['name']}")
