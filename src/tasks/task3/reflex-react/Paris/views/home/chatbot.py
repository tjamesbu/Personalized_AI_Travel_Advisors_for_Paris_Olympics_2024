from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('env'), override=True)

import reflex as rx
from Paris.styles.styles import Size
from Paris.styles.fonts import Font
from Paris.styles.colors import Color, TextColor


from state import QA, State

class LoadingIcon(rx.Component):
    """A custom loading icon component."""

    library = "react-loading-icons"
    tag = "SpinningCircles"
    stroke: rx.Var[str]
    stroke_opacity: rx.Var[str]
    fill: rx.Var[str]
    fill_opacity: rx.Var[str]
    stroke_width: rx.Var[str]
    speed: rx.Var[str]
    height: rx.Var[str]

    def get_event_triggers(self) -> dict:
        return {"on_change": lambda status: [status]}

loading_icon = LoadingIcon.create

def chatbot() -> rx.Component:
    return rx.chakra.vstack(
        rx.heading("AI assistant", margin_bottom="1em"),
        # navbar(),
        action_bar(),
        chat(),
        # action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="80vh",  # % of the viewable page height
        align_items="stretch",
        spacing="0",
        width="25%", # I specified 75% for the vstack, but the action bar sticks out ??? 
    )

message_style = dict(
    display="inline-block", 
    padding="1em", 
    border_radius="8px", 
    max_width=["30em", "30em", "50em", "50em", "50em", "50em"]
)


def message(qa: QA) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.box(
        rx.box(
            rx.markdown(
                qa.question,
                background_color=rx.color("mauve", 4),
                color=rx.color("mauve", 12),
                **message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        rx.box(
            rx.markdown(
                qa.answer,
                background_color=rx.color("accent", 4),
                color=rx.color("accent", 12),
                **message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.box(
            rx.foreach(State.chats[State.current_chat], message), 
            width="100%",
            ),
        py="8",
        flex="1",
        width="100%",
        max_width="50em",
        padding_x="4px",
        align_self="stretch",
        overflow="hidden",
        padding_bottom="1em",
        padding_left="1em",
        padding_top="1em",
        align="stretch"  # JP
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.center(
        rx.vstack(
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.hstack(
                        rx.radix.text_field(
                            rx.radix.text_field(
                                placeholder="Type your question...",
                                id="question",
                                width=["15em", "20em", "45em", "50em", "50em", "50em"],
                            ),
                            rx.radix.text_field.slot(
                                rx.tooltip(
                                    rx.icon("info", size=18),
                                    content="Enter your question",
                                    # font_size="1.5em",  # doesn't work
                                )
                            ),
                        ),
                        rx.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.text("Send", 
                                        # font_size="1em"  # doesn't work
                                        ),
                            ),
                            type="submit",
                        ),
                        align_items="center",
                    ),
                    is_disabled=State.processing,
                ),
                on_submit=State.process_question,
                reset_on_submit=True,
            ),
            rx.text(
                "AI may return factually incorrect or misleading responses. Use discretion.",
                text_align="center",
                # flex_wrap="wrap",  # JP - doesn't work
                font_size="1.5em",
                color=rx.color("mauve", 10),
            ),
            # rx.logo(margin_top="-1em", margin_bottom="-1em"),
            align_items="center",
        ),
        position="sticky",  # JP no need, it was for when the action bar was at the bottom
        bottom="0",
        left="0",
        padding_y="16px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        align_items="stretch",
        width="100%",
    )
