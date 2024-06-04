from enum import Enum

# https://imagecolorpicker.com/color-code/060606

class Color(Enum):
    ACCENT = "#060606" #"#5690bb" # steel blue 
    PRIMARY = "#bb9a56"
    SECONDARY = "#fefef5"
    TERTIARY = "#fec6c7"
    CUARTIARY = "#092f31"


class TextColor(Enum):
    ACCENT = "#060606 !important"  # cod gray ~ black
    PRIMARY = "#fefef5"  # light yellow
    SECONDARY = "#bb9a56" # dark yellow
    TERTIARY = "#fec6c7"  # dark red
    CUARTIARY = "#092f31"  # bottle green
