import streamlit as st
from streamlit_sortables import sort_items
from functions.utility import (
    get_data,
    get_card,
    add_selected_card,
    is_card_selected_or_in_use,
)


def run():
    with st.container():
        st.markdown("# Cards")
        players = get_data("players")
        player_tabs = st.tabs([player["character"] for player in players])
        for player, player_tab in zip(players, player_tabs):
            print("player", player)
            is_my_cards = False
            if player["character"] == st.session_state["player"]["character"]:
                is_my_cards = True
            with player_tab:
                player_cards = player["cards"]
                if is_my_cards:
                    ...
                    if "sorted_cards" in st.session_state:
                        if st.session_state["sorted_cards"]:
                            sorted_cards = st.session_state["sorted_cards"][0]["items"]
                            print("sorted", sorted_cards)
                            # if sorted_cards != player_cards:
                            #     player_cards = sorted_cards
                            #     player["cards"] = sorted_cards
                            #     update_players(players)
                card_row_1 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
                card_row_2 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
                for card_column, card_id in zip(card_row_1 + card_row_2, player_cards):
                    with card_column:
                        card = get_card(card_id)
                        if is_my_cards:
                            card_image = card["image"]
                            card_name = f'{card["name"]} [{card_id}]'
                        else:
                            card_image = "red_joker"
                            card_name = ""

                        st.button(
                            "Select",
                            key=f'select_{card["id"]}',
                            on_click=add_selected_card,
                            kwargs={"card_id": card["id"]},
                            disabled=is_card_selected_or_in_use(card_id=card["id"]),
                        )
                        st.image(
                            f"data/card_images/{card_image}.png",
                            caption=card_name,
                        )
                if is_my_cards:
                    original_items = [
                        {
                            "header": "Drag and Drop to Reorder Cards",
                            "items": [card for card in player_cards],
                        }
                    ]
                    sorted_items = sort_items(
                        original_items, multi_containers=True, key="sorted_cards"
                    )
                    # st.write(st.session_state["sorted_cards"])

        # original_items = [
        #     {"header": "first container", "items": ["A", "B", "C"]},
        #     {"header": "second container", "items": ["D", "E", "F"]},
        # ]

        # sorted_items = sort_items(original_items, multi_containers=True, key="sort_key")

        # st.write(f"original_items: {original_items}")
        # st.write(f"sorted_items: {sorted_items}")
        # st.write(st.session_state["sort_key"])
