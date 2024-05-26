import reflex as rx
# from Paris.views.navbar import navbar
from Paris.views.home.header import header_with_image_and_text
from Paris.views.home.recommendations import recommendations
from Paris.views.home.location import location
from Paris.views.footer import footer_desktop
from Paris.views.home.chatbot import chatbot
from Paris.components.black_line import black_line

@rx.page(
    route="/", 
    title="The best AI trip planner",
    description="Homepage"
    )
def home() -> rx.Component:
    return rx.box(
        # navbar(),
        header_with_image_and_text(),
        rx.hstack(
            rx.vstack(
                location(),
                recommendations(),
                black_line(),
                # contact(),
                black_line(),
                width="75%",
            ),
            chatbot(),
        ),
        black_line(),
        footer_desktop(),
    )
