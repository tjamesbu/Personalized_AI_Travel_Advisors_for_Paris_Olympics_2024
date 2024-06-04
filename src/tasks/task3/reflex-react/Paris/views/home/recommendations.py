import reflex as rx
from Paris.components.title import title
from Paris.components.foto_info import foto_info
from Paris.styles.styles import Size

def recommendations() -> rx.Component:
    return rx.vstack(
        title("A few ideas for you"),
        rx.chakra.responsive_grid(
                rx.chakra.box(
                    foto_info(
                        "/entrada.jpg",
                        "Restaurant entrance",
                        """AI-generated description"""  
                    )                      
                ),
                rx.chakra.box(
                    foto_info(
                        "/jardin.jpg",
                        "Wine barrel and clay over",
                        """AI-generated description"""                            
                    )                                                
                ),
                rx.chakra.box(
                    foto_info(
                        "/cava.jpg",
                        "Wine cave",
                        """AI-generated description"""
                    )                                                
                ),
                columns=[1, 3],      
                direction="row",
                justify="center",
                width="100%"
            ),
        align_items="center",
        )
