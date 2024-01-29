from PIL import Image, ImageDraw
from typing import Tuple


def get_ellipse_coords(point: Tuple[int, int]) -> Tuple[int, int, int, int]:
    scale_factor = 1
    center = point[0] * scale_factor, point[1] * scale_factor
    radius = 20
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )
