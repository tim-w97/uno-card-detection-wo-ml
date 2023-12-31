from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from enum import Enum
from uno_classes import Color


def determine_color(color_bgr):
    class OriginalUnoColors(Enum):
        RED = sRGBColor(198, 42, 53)
        YELLOW = sRGBColor(239, 211, 46)
        GREEN = sRGBColor(88, 166, 54)
        BLUE = sRGBColor(3, 93, 172)

    color_to_compare = sRGBColor(color_bgr[2], color_bgr[1], color_bgr[0])

    min_diff = None
    color = None

    for uno_color in OriginalUnoColors:
        # Convert from RGB to Lab Color Space
        color1_lab = convert_color(color_to_compare, LabColor)
        color2_lab = convert_color(uno_color.value, LabColor)

        # Find the color difference
        diff = delta_e_cie2000(color1_lab, color2_lab)

        if min_diff is None or diff < min_diff:
            min_diff = diff
            color = Color[uno_color.name]

    return color
