import reflex as rx

from Paris.styles.styles import Size
from Paris.styles.fonts import Font
from Paris.styles.colors import Color, TextColor

def header_with_image_and_text() -> rx.Component:
    return rx.hstack(
        rx.link(
                rx.image(
                    src="/logo.png",
                    alt="logo",
                    width="12em",
                    margin_left=["0em","1em"],
                    margin_top=["0em","1em"],
                    # align_items="center"
                ),
                href="/",
            ),

        rx.text(
            "Best AI trips", 
            align="left", 
            size="9", 
            width="150%",
            as_="div",
            font_family=Font.TITLE.value,
            margin_top=Size.SMALL.value,
            text_color=TextColor.SECONDARY.value,
            padding_x="1em",
            # padding_y=["0em","14em"],
            ),
            
        bg="center/cover url('/paris_olympics.png')",
        height=["25em","45em"],
        pos="relative",
        align_items="top",
        margin_top="0px",
        top="0",
        z_index="999",
    )

