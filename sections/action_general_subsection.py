import streamlit as st
from functions.utility import (
    read_yaml,
    get_data,
    set_general_action,
    show_hand_to_character,
)

from icecream import ic


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    characters = get_data("characters")
    player_character = characters[players[player_code]["character"]]
    is_current_turn = players[player_code]["current_turn"]
    game = get_data("game", game_code=game_code)
    is_game_started = game["is_started"]
    help = "Select general actions"
    st.title("General Actions", help=help)
    action_buttons = read_yaml("data/action_buttons.yaml")
    button_columns_row_1 = st.columns([1, 1, 1, 1, 1])
    button_columns_row_2 = st.columns([1, 1, 1, 1, 1])
    for action_button, button_column in zip(
        action_buttons, button_columns_row_1 + button_columns_row_2
    ):
        with button_column:
            st.image(action_button["image"])
            is_pre_start_only = action_button.get("is_pre_start_only")
            is_post_start_only = action_button.get("is_post_start_only")
            is_current_turn_only = action_button.get("is_current_turn_only")
            is_not_current_turn_only = action_button.get("is_not_current_turn_only")
            is_side = action_button.get("is_side")
            button_enabled = True
            # ic(is_game_started)
            # ic(action_button["name"])
            # ic(button_enabled)
            if button_enabled and is_pre_start_only and not is_game_started:
                button_enabled = True
                # ic("set1")
            # ic(button_enabled)
            if button_enabled and is_pre_start_only and is_game_started:
                button_enabled = False
                # ic("set2")
            # ic(button_enabled)
            if button_enabled and is_post_start_only and not is_game_started:
                button_enabled = False
                # ic("set3")
            # ic(button_enabled)
            # if button_enabled and is_post_start_only and is_game_started:
            #     button_enabled = False
            #     ic("set4")
            # ic(button_enabled)
            if button_enabled and is_current_turn_only and is_game_started:
                button_enabled = is_current_turn
                # ic("set5")
            elif (
                button_enabled and is_not_current_turn_only == True and is_game_started
            ):
                button_enabled = not is_current_turn
                # ic("set6")
            # ic(button_enabled)
            if button_enabled and is_side:
                if is_side != player_character["side"]:
                    button_enabled = False
                    # ic("set7")
            # ic(button_enabled)

            disabled = not button_enabled
            st.button(
                action_button["name"],
                use_container_width=True,
                on_click=set_general_action,
                kwargs={"action": action_button["name"]},
                disabled=disabled,
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
