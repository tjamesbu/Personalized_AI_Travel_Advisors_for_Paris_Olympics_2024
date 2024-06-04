import reflex as rx
from Paris.components.icon import link_icon_footer
from Paris.views.constants import INSTAGRAM_URL, WHATSAPP_URL

def footer_desktop():
    return rx.flex(
                rx.image(
                    src="/logo.png",
                    alt=" logo",
                    width="8em",
                    margin_left=["0em","1em"],
                    margin_top=["0em","1em"],
                    # align_items="center"
                ),
                rx.spacer(),
                rx.spacer(),
                rx.tablet_and_desktop(
                rx.flex(
                    link_icon_footer(
                    "/ig.png",
                    "Instagram logo",
                    INSTAGRAM_URL                 
                    ),
                    link_icon_footer(
                    "/wpp.png",
                    " WHATSApp logo",
                    WHATSAPP_URL
                    ),
                direction="row", # default horizontal alignment
                justify="center",
                spacing="4",
                class_name="footer-icons",
                ),
                ),                
                rx.spacer(),
                rx.link(
                    "©Site created by Jean-Pierre Bianchi",
                    # href="https://xxx.com",
                    is_external=True,
                    margin="1em",
                    color="#828282"
                        ),
                columns=[1,3],
                bg="#393a3d",
                direction="row", # default horizontal alignment
                justify="between",
                align="center",
                class_name="footer-container",
                width="100%",
            )
    
