import streamlit as st
from functions.utility import get_data, set_data, add_activity
from streamlit_image_coordinates import streamlit_image_coordinates
from functions.board import get_ellipse_coords
from PIL import Image, ImageDraw


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    characters = get_data("characters")
    positions = players[player_code]["positions"]
    with Image.open("checkerboard.png") as img:
        draw = ImageDraw.Draw(img)
        # Draw an ellipse at each coordinate in position
        for player in players.values():
            inner_colors = [
                characters[player["character"]]["marker_color_code"],
                None,
            ]
            outer_colors = [
                None,
                characters[player["character"]]["marker_color_code"],
            ]

            for point, inner_color, outer_color in zip(
                player["positions"], inner_colors, outer_colors
            ):
                coords = get_ellipse_coords(point)
                draw.ellipse(coords, fill=inner_color, outline=outer_color, width=5)

        value = streamlit_image_coordinates(img, key="pil")

        if value is not None:
            position = [value["x"], value["y"]]

            if position not in positions:
                positions.insert(0, position)
                del positions[2:]
                set_data("players", players, game_code=game_code)
                add_activity("Moved")
                st.rerun()
