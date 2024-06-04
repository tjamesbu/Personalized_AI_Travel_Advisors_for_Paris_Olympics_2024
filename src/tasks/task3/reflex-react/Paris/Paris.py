import reflex as rx
from rxconfig import config
from Paris.pages.home import home
# from Paris.pages.menu import menu
# from Paris.pages.reservas import reservas
# from Paris.pages.nosotros import nosotros
import Paris.styles.styles as styles

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


app = rx.App(
    stylesheets=styles.STYLESHEETS,
    style=styles.BASE_STYLE,
    # theme=rx.theme(appearance="dark")
)
