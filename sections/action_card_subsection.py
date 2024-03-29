import streamlit as st
from functions.utility import (
    read_yaml,
    get_data,
    get_card_owner,
    get_card,
    set_action,
    show_card_to_character,
    give_card_to_character,
)
import random
import string
from icecream import ic


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    selected_cards = players[player_code]["selected_cards"]
    is_current_turn = players[player_code]["current_turn"]

    help = "Select a card from your hand or from other players and then choose an action for the individual card."
    st.title("Selected Card Actions", help=help)
    card_action_buttons = read_yaml("data/card_action_buttons.yaml")

    card_columns = st.columns([1, 1, 1, 1, 1])
    button_columns_row_1 = st.columns(
        [
            1,
            1,
            1,
            1,
        ]
    )
    button_columns_row_2 = st.columns(
        [
            1,
            1,
            1,
            1,
        ]
    )
    button_columns_row_3 = st.columns(
        [
            1,
            1,
            1,
            1,
        ]
    )
    for card_id, card_column in zip(selected_cards, card_columns):
        my_cards = players[player_code]["cards"]
        with card_column:
            card = get_card(card_id)
            is_battle_point = card.get("battle_point")
            if card_id in my_cards:
                is_card_owner = True
                card_image = card["image"]
                card_name = card["name"]
            else:
                is_card_owner = False
                card_owner = get_card_owner(card_id)
                card_image = "Reverse"
                card_name = f"<{card_owner['character']} Card>"

            st.image(
                f"static/card_images/{card_image}.png",
                caption=card_name,
            )
    if selected_cards:
        for button, button_col in zip(
            card_action_buttons,
            button_columns_row_1 + button_columns_row_2 + button_columns_row_3,
        ):
            with button_col:
                button_enabled = True
                is_current_turn_only = button.get("is_current_turn_only")
                is_card_owner_only = button.get("is_card_owner_only")
                is_not_card_owner_only = button.get("is_not_card_owner_only")
                is_not_current_turn_only = button.get("is_not_current_turn_only")
                is_battle_card_only = button.get("is_battle_card_only")
                if button_enabled and is_current_turn_only:
                    button_enabled = is_current_turn
                if button_enabled and is_card_owner_only:
                    button_enabled = is_card_owner
                if button_enabled and is_not_card_owner_only:
                    button_enabled = not is_card_owner
                if button_enabled and is_not_current_turn_only:
                    button_enabled = not is_current_turn
                if button_enabled and is_battle_card_only:
                    button_enabled = is_battle_point
                rid = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=6)
                )
                disabled = not button_enabled
                st.button(
                    button["name"],
                    key=f"{rid}_{card_id}",
                    use_container_width=True,
                    on_click=set_action,
                    kwargs={"action": button["name"], "card_id": card_id},
                    disabled=disabled,
                )
        if "show_card_to_character" in st.session_state:
            st.session_state.pop("show_card_to_character")
            options = [
                player["character"]
                for player in players.values()
                if player["player_code"] != player_code
            ]
            st.selectbox(
                "Select Character to Show Card",
                index=None,
                key="show_card_to_character",
                options=options,
                on_change=show_card_to_character,
                kwargs={"card_id": card_id},
            )
        if "give_card_to_character" in st.session_state:
            st.session_state.pop("give_card_to_character")
            options = [
                player["character"]
                for player in players.values()
                if player["player_code"] != player_code
            ]
            st.selectbox(
                "Select Character to Give Card",
                index=None,
                key="give_card_to_character",
                options=options,
                on_change=give_card_to_character,
                kwargs={"card_id": card_id},
            )
