import streamlit as st
from functions.utility import (
    get_data,
)


def run():
    game_stats = st.container(border=True, height=420)
    with game_stats:
        st.title("Game Stats")
        metric_columns_1 = st.columns([1, 1, 1, 1, 1, 1])
        metric_columns_2 = st.columns([1, 1, 1, 1, 1, 1])
        chart_columns = st.columns([1, 1, 1])
        game_code = st.query_params.game
        draw_pile = get_data("draw_pile", game_code=game_code)
        discards = get_data("discards", game_code=game_code)
        activities = get_data("activities", game_code=game_code)
        activities = [
            activity for activity in activities if activity["type"] == "system"
        ]
        players = get_data("players", game_code=game_code)
        activities_by_players = {
            f'Activities | {player["character"]}': 0 for player in players.values()
        }
        for activity in activities:
            character = activity["player"]["character"]
            activities_by_players[f"Activities | {character}"] += 1
        game = get_data("game", game_code=game_code)
        game_stats = game["stats"]
        game_stats = {
            "Draw Pile": len(draw_pile),
            "Discard Pile": len(discards),
            **game_stats,
            **activities_by_players,
        }
        for (stat, value), metric_column in zip(
            game_stats.items(), metric_columns_1 + metric_columns_2
        ):
            with metric_column:
                st.metric(stat, value)

        game_metrics = game["metrics"]
        for (metric, data), chart_column in zip(game_metrics.items(), chart_columns):
            with chart_column:
                st.write(metric)
                data = {"roll": list(data.keys()), "rolls": list(data.values())}
                st.bar_chart(
                    data,
                    x="roll",
                    y="rolls",
                    height=150,
                    use_container_width=True,
                )
