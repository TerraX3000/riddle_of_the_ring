import streamlit as st
from functions.utility import (
    get_data,
    set_data,
    get_card,
    transfer_card,
)
from icecream import ic


def show_riddler_card():
    game_code = st.query_params.game
    riddle_power_play = get_data("riddle_power_play", game_code=game_code)
    riddle_power_play["can_riddler_see_card"] = True
    set_data("riddle_power_play", riddle_power_play, game_code=game_code)
    return


def end_riddle():
    game_code = st.query_params.game
    set_data("riddle_power_play", {}, game_code=game_code)
    return


def give_card_to_riddler(card_id, character):
    transfer_card(card_id=card_id, character=character)
    end_riddle()
    return


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
        card_id = riddle_power_play["riddle_card"]
        try:
            can_riddler_see_card = riddle_power_play["can_riddler_see_card"]
        except:
            can_riddler_see_card = False

        if is_riddler or is_owner:
            help = """Cards in this section are only visible to the indicated player."""
            st.title("Riddle Power Play", help=help)
            placeholder = st.empty()
            riddle_button_1, riddle_button_2, unused_column = st.columns([1, 1, 1])

            if is_riddler:
                placeholder.info(f"{riddler} is riddling {card_owner}'s card.")
                with riddle_button_1:
                    st.button(
                        "End Riddle",
                        on_click=end_riddle,
                        use_container_width=True,
                    )

            if is_owner:
                placeholder.info(
                    f"""
            No one else can see your card.\n
            If the riddler does not guess your card, show the riddler the card.\n
            If the riddler guesses the card, give the card to the riddler.
            """
                )
                with riddle_button_1:
                    st.button(
                        "Show riddler the card",
                        on_click=show_riddler_card,
                        use_container_width=True,
                    )
                with riddle_button_2:
                    st.button(
                        "Give card to riddler",
                        on_click=give_card_to_riddler,
                        kwargs={"card_id": card_id, "character": riddler},
                        use_container_width=True,
                    )

            table_card_columns = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

            card_col = table_card_columns[0]
            with card_col:
                card = get_card(card_id)

                if is_riddler and not can_riddler_see_card:
                    card_image = "Reverse"
                    card_name = f"<{card_owner} Card>"

                elif is_owner or (is_riddler and can_riddler_see_card):
                    card_image = card["image"]
                    card_name = f"{card['name']} ({card_owner})"

                st.image(
                    f"static/card_images/{card_image}.png",
                    caption=f"{card_name}",
                )
