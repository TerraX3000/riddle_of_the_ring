import streamlit as st
from sections import (
    player_section,
    cards_section,
    action_section,
    board_section,
    activity_section,
    discard_section,
    battle_section,
)
from functions.utility import (
    show_battle_section,
    initialize_game_data,
    get_shuffled_deck,
)

st.set_page_config(
    page_title="Riddle of the Ring",
    layout="wide",
)

style = """<style>h2,h3,h4,h5,h6 {text-align: center;}</style>"""
st.markdown(style, unsafe_allow_html=True)

if "is_initialized" not in st.session_state:
    print("+++++ Initializing session +++++++")
    st.session_state["is_initialized"] = True
    st.session_state["points"] = []
    player = {}
    player["id"] = 1
    player["character"] = "Merry"
    st.session_state["player"] = player
    st.session_state["selected_cards"] = []
    # st.session_state["in_use_cards"] = []
    st.session_state["attacker_cards"] = []
    st.session_state["defender_cards"] = []
    initialize_game_data(category="players")
    initialize_game_data(category="activities", data=[])
    initialize_game_data(category="characters")
    initialize_game_data(category="draw_pile", data=get_shuffled_deck())
    initialize_game_data(category="discards", data=[])

st.header("Riddle of the Ring")

col_1, col_2, col_3 = st.columns([0.1, 0.5, 0.4])

with col_1:
    player_section.run()

with col_2:
    cards_section.run()

with col_3:
    action_section.run()

if show_battle_section():
    with st.container():
        st.markdown("# Battle")
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                battle_section.run("attacker")
            with col2:
                battle_section.run("defender")

col_4, col_5, col_6 = st.columns([1, 3, 1])

with col_4:
    activity_section.run()

with col_5:
    board_section.run()

with col_6:
    discard_section.run()
