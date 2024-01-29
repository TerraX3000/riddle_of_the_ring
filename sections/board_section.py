import streamlit as st
from functions.utility import get_data
from streamlit_image_coordinates import streamlit_image_coordinates
from functions.board import get_ellipse_coords
from PIL import Image, ImageDraw


def run():
    with Image.open("checkerboard.png") as img:
        draw = ImageDraw.Draw(img)
        # Draw an ellipse at each coordinate in points
        colors = ["blue", "green"]
        for point, color in zip(st.session_state["points"], colors):
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill=color)

        value = streamlit_image_coordinates(img, key="pil")

        if value is not None:
            point = value["x"], value["y"]

            if point not in st.session_state["points"]:
                st.session_state["points"].insert(0, point)
                print(st.session_state["points"])
                st.experimental_rerun()
