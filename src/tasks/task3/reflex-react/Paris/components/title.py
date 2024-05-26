import reflex as rx
import Paris.styles.styles as styles
from Paris.styles.styles import Size

def title(text: str, **kwargs) -> rx.Component:
    return rx.heading(
                rx.hstack(
                    rx.text(text),        
                    ),
                    align="left",
                    padding=["0.3em",Size.SMALL.value],
                    margin_top=Size.MEDIUM.value,
                    style=styles.title_style,
                    **kwargs  # JP added it to modify style on the go
                )
    
def subtitle(text: str) -> rx.Component:
    return rx.heading(
                rx.hstack(
                    rx.text(text),        
                    ),
                    align="left",
                    padding_top=Size.MEDIUM.value,
                    padding_bottom="0.3em",
                    style=styles.subtitle_style
                )

def drinks_title(text) -> rx.Component:
    return rx.heading(
                rx.hstack(
                    rx.text(text),        
                    ),
                    align="left",
                    padding_top=Size.SMALL.value,
                    style=styles.drinktitle_style
                )
    