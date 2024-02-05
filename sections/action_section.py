import streamlit as st
from functions.utility import (
    get_data,
    get_card_owner,
    get_card,
    get_item,
    get_player_cards,
    set_action,
    set_general_action,
    unselect_all_cards,
    add_activity,
    show_hand_to_character,
)
from icecream import ic


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    with st.container(border=True):
        help = "Select general actions"
        st.title("Actions", help=help)
        st.selectbox(
            "Select Action",
            index=None,
            key=f"general_action",
            options=[
                "Roll Die",
                "Draw Card",
                "Show Hand to Player",
                "Attack from Good City",
                "Attack from Evil City",
                "Defend from Good City",
                "Defend from Evil City",
                "Surrender",
            ],
            on_change=set_general_action,
        )
        if "show_hand_to_character" in st.session_state:
            st.session_state.pop("show_hand_to_character")
            options = [
                player["character"]
                for player in players.values()
                if player["player_code"] != player_code
            ]
            st.selectbox(
                "Select Character to Show Hand",
                index=None,
                key="show_hand_to_character",
                options=options,
                on_change=show_hand_to_character,
            )

    with st.container(border=True):
        help = (
            "Select cards from your hand and then choose actions for individual cards."
        )
        st.title("Selected Cards", help=help)
        for card_id in players[player_code]["selected_cards"]:
            my_cards = players[player_code]["cards"]
            with st.container():
                col_1, col_2 = st.columns([1, 2])
                if card_id in my_cards:
                    card = get_card(card_id)
                    card_name = card["name"]
                else:
                    card_owner = get_card_owner(card_id)
                    card_name = f"<{card_owner['character']} Card>"
                card = get_card(card_id)
                col_1.write(card_name)
                col_2.selectbox(
                    "Select Action",
                    index=None,
                    key=f"action_{card_id}",
                    options=[
                        "Unselect",
                        "Retain",
                        "Discard",
                        "Power Play",
                        "Use to Attack",
                        "Use to Defend",
                        "In Use",
                        "Use Spy",
                        "Use Riddle",
                        "Show Card to Player",
                        "Take for Friendly Exchange",
                    ],
                    label_visibility="collapsed",
                    kwargs={"card_id": card_id},
                    on_change=set_action,
                )
        if players[player_code]["selected_cards"]:

            st.button(
                "Unselect all cards",
                on_click=unselect_all_cards,
                use_container_width=True,
            )
        else:
            st.markdown("*Select cards in your hand to perform card-specific actions*")
