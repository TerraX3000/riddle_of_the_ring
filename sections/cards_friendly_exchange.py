import streamlit as st
from functions.utility import (
    get_data,
    set_data,
    get_card,
    get_card_owner,
    transfer_card,
)
from icecream import ic


def complete_friendly_exchange(
    first_party, second_party, first_party_card, second_party_card
):
    game_code = st.query_params.game
    transfer_card(first_party_card, first_party)
    transfer_card(second_party_card, second_party)
    set_data("friendly_exchange", {}, game_code=game_code)
    return


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    this_character = players[player_code]["character"]
    friendly_exchange = get_data("friendly_exchange", game_code=game_code)
    if friendly_exchange:
        status = friendly_exchange["status"]
        first_party = friendly_exchange["first_party"]
        second_party = friendly_exchange["second_party"]
        former_card_owners = [second_party, first_party]
        new_card_owners = [first_party, second_party]
        if this_character in [first_party, second_party]:
            help = """Cards in this section are only visible to the indicated player."""
            st.title("Friendly Exchange", help=help)
            info_message = st.container()
            info_message.info(
                f"Friendly exchange between {first_party} and {second_party}"
            )
            placeholder = st.empty()
            button_column_1, unused = st.columns([1, 2])
            card_columns = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

            if status.lower() == "ready":
                placeholder.empty()
                first_party_card = friendly_exchange[first_party]["card"]
                second_party_card = friendly_exchange[second_party]["card"]
                cards = [first_party_card, second_party_card]

                if this_character == first_party:
                    with button_column_1:
                        st.button(
                            "Complete Friendly Exchange",
                            on_click=complete_friendly_exchange,
                            kwargs={
                                "first_party": first_party,
                                "second_party": second_party,
                                "first_party_card": first_party_card,
                                "second_party_card": second_party_card,
                            },
                            use_container_width=True,
                        )

                for card_id, former_card_owner, new_card_owner, card_col in zip(
                    cards, former_card_owners, new_card_owners, card_columns
                ):
                    with card_col:
                        card = get_card(card_id)

                        st.image(
                            f"static/card_images/{card['image']}.png",
                            caption=f"{card['name']} (From {former_card_owner} to {new_card_owner})",
                        )
            elif status.lower() == "pending":
                placeholder.info(
                    f"Friendly exxhange is pending card selection by {second_party}"
                )
