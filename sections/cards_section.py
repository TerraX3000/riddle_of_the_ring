import streamlit as st
from streamlit_sortables import sort_items
from functions.utility import (
    get_data,
    get_card,
    add_selected_card,
    is_card_selected_or_in_use,
    set_data,
)
from collections import OrderedDict
from icecream import ic
from sections import (
    cards_subsection,
    cards_table_subsection,
    cards_show_to_player_subsection,
    cards_riddle_subsection,
)


def run():
    card_container = st.container(border=True)
    riddle_power_play_container = st.container(border=True)
    show_card_container = st.container(border=True)
    table_cards_container = st.container(border=True)
    with card_container:
        cards_subsection.run()
    with riddle_power_play_container:
        cards_riddle_subsection.run()
    with show_card_container:
        cards_show_to_player_subsection.run()
    with table_cards_container:
        cards_table_subsection.run()
