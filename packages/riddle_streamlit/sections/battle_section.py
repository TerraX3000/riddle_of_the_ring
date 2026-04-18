import streamlit as st
from functions.utility import (
    get_data,
    remove_battle_card,
    get_card,
    discard_battle_card,
    retain_battle_card,
)
from icecream import ic


def run(battle_role):
    st.markdown(f"## {battle_role.title()}")
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
    battle_card_columns = st.columns(
        [
            1,
            1,
            1,
            1,
            1,
        ]
    )
    for (
        card_id,
        card_col,
    ) in zip(battle[f"{battle_role}_cards"], battle_card_columns):
        with card_col:
            card = get_card(card_id)
            if card.get("type") == "City Battlepoint":
                st.button("Discard", disabled=True)
                st.button(
                    "Clear",
                    key=f'battle_{battle_role}_remove_{card["id"]}',
                    on_click=remove_battle_card,
                    kwargs={"card_id": card["id"], "battle_role": battle_role},
                )
            else:
                st.button(
                    "Discard",
                    key=f'battle_{battle_role}_discard_{card["id"]}',
                    on_click=discard_battle_card,
                    kwargs={"card_id": card["id"], "battle_role": battle_role},
                )
                st.button(
                    "Retain",
                    key=f'battle_{battle_role}_retain_{card["id"]}',
                    on_click=retain_battle_card,
                    kwargs={"card_id": card["id"], "battle_role": battle_role},
                )
            st.image(
                f"static/card_images/{card['image']}.png",
                caption=card["name"],
            )
