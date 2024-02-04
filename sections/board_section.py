import streamlit as st
from functions.utility import get_data, set_data
from streamlit_image_coordinates import streamlit_image_coordinates
from functions.board import get_ellipse_coords
from PIL import Image, ImageDraw


def run():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    positions = players[player_code]["positions"]
    with Image.open("checkerboard.png") as img:
        draw = ImageDraw.Draw(img)
        # Draw an ellipse at each coordinate in position
        for player in players.values():
            colors = ["blue", "green"]
            for point, color in zip(player["positions"], colors):
                coords = get_ellipse_coords(point)
                draw.ellipse(coords, fill=color)

        value = streamlit_image_coordinates(img, key="pil")

        if value is not None:
            position = [value["x"], value["y"]]

            if position not in positions:
                positions.insert(0, position)
                del positions[2:]
                set_data("players", players, game_code=game_code)
                st.rerun()
