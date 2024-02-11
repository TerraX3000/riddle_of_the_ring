import streamlit as st
from functions.utility import (
    read_yaml,
    get_data,
    get_card_owner,
    get_card,
    set_action,
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
            if card_id in my_cards:
                is_card_owner = True
                card = get_card(card_id)
                card_image = card["image"]
                card_name = card["name"]
            else:
                is_card_owner = False
                card_owner = get_card_owner(card_id)
                card_image = "red_joker"
                card_name = f"<{card_owner['character']} Card>"
            card = get_card(card_id)
            st.image(
                f"data/card_images/{card_image}.png",
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
                is_not_card_only_owner = button.get("is_not_card_only_owner")
                is_not_current_turn_only = button.get("is_not_current_turn_only")
                if button_enabled and is_current_turn_only:
                    button_enabled = is_current_turn
                if button_enabled and is_card_owner_only:
                    button_enabled = is_card_owner
                if button_enabled and is_not_card_only_owner:
                    button_enabled = not is_card_owner
                if button_enabled and is_not_current_turn_only:
                    button_enabled = not is_current_turn
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
