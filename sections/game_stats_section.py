import streamlit as st
from functions.utility import (
    get_data,
)


def run():
    game_stats = st.container(border=True, height=420)
    with game_stats:
        st.title("Game Stats")
        metric_columns_1 = st.columns([1, 1, 1, 1, 1])
        metric_columns_2 = st.columns([1, 1, 1, 1, 1])
        game_code = st.query_params.game
        draw_pile = get_data("draw_pile", game_code=game_code)
        discards = get_data("discards", game_code=game_code)
        game_stats = get_data("game", game_code=game_code)["stats"]
        game_stats = {
            "Draw Pile": len(draw_pile),
            "Discard Pile": len(discards),
            **game_stats,
        }
        for (stat, value), metric_column in zip(
            game_stats.items(), metric_columns_1 + metric_columns_2
        ):
            with metric_column:
                st.metric(stat, value)
