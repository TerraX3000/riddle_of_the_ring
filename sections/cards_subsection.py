import streamlit as st
from streamlit_sortables import sort_items
from functions.utility import (
    get_data,
    get_card,
    add_selected_card,
    is_card_selected_or_in_use,
    set_data,
    shuffle_player_cards,
)
from collections import OrderedDict
from icecream import ic


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    help = """View your cards and select cards for card-specific actions.
    Tabs show cards for other players which are hidden unless you are 
    permitted to see their cards (e.g., using a Spy to see their cards)."""
    st.title("Player Cards", help=help)
    players = get_data("players", game_code=game_code)
    ordered_players = OrderedDict(players)
    ordered_players.move_to_end(player_code, last=False)
    placeholder = st.empty()
    player_tabs = st.tabs([player["character"] for player in ordered_players.values()])
    for player, player_tab in zip(ordered_players.values(), player_tabs):
        is_my_cards = False
        is_show_hand_to_character = False
        if player["character"] == players[player_code]["character"]:
            is_my_cards = True
        if (
            player["special_actions"]["show_hand_to_character"]
            == players[player_code]["character"]
        ):
            is_show_hand_to_character = True
            player["special_actions"]["show_hand_to_character"] = None

        with player_tab:
            player_cards = player["cards"]
            if is_show_hand_to_character:
                placeholder.info(f"{player['character']} is showing hand to you.")
            card_row_1 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            if len(player_cards) > 10:
                st.divider()
                st.markdown(
                    "*Just a friendly reminder: Over 10 Card Limit - Remember to Discard* :sunglasses:"
                )
            card_row_2 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            for selected_card_index, (card_column, card_id) in enumerate(
                zip(card_row_1 + card_row_2, player_cards)
            ):
                with card_column:
                    card = get_card(card_id)
                    if is_my_cards or is_show_hand_to_character:
                        card_image = card["image"]
                        card_name = f'{card["name"]} [{card_id}]'
                    else:
                        card_image = "Reverse"
                        card_name = ""

                    st.button(
                        "Select",
                        key=f'select_{card["id"]}',
                        on_click=add_selected_card,
                        kwargs={
                            "card_id": card["id"],
                            "selected_card_index": selected_card_index,
                            "card_owner_player_code": player["player_code"],
                        },
                        disabled=is_card_selected_or_in_use(card_id=card["id"]),
                    )
                    st.image(
                        f"static/card_images/{card_image}.png",
                        caption=card_name,
                    )
            if is_my_cards:
                st.button("Shuffle my cards", on_click=shuffle_player_cards)

    set_data("players", players, game_code=game_code)
