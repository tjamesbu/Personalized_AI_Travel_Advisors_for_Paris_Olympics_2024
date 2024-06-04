import gradio as gr
import pycountry
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="city_selector")

def get_country_list():
    countries = list(pycountry.countries)
    return sorted([country.name for country in countries])

def get_state_list(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        subdivisions = list(pycountry.subdivisions.get(country_code=country.alpha_2))
        return sorted([subdivision.name for subdivision in subdivisions])
    except AttributeError:
        return []

def get_city_suggestions(state_name, country_name):
    query = f"{state_name}, {country_name}"
    locations = geolocator.geocode(query, exactly_one=False, limit=100)
    if locations:
        return sorted({location.address.split(',')[0] for location in locations})
    else:
        return ["No matching cities found."]

def city_selected(city_name):
    location = geolocator.geocode(city_name)
    if location:
        return f"Selected City: {location.address}"
    else:
        return "City not found. Please try again."

with gr.Blocks() as demo:
    country_input = gr.Dropdown(label="Select a country", choices=get_country_list())
    state_input = gr.Dropdown(label="Select a state", interactive=True)
    city_input = gr.Dropdown(label="Select a city", interactive=True)
    output = gr.Textbox(label="Output")
    
    def update_states(country):
        states = get_state_list(country)
        return gr.update(choices=states)

    # def update_cities(state, country):
    #     cities = get_city_suggestions(state, country)
    #     return gr.update(choices=cities)

    country_input.change(fn=update_states, inputs=country_input, outputs=state_input)
    state_input.change(fn=lambda state: update_cities(state, country_input.value), inputs=state_input, outputs=city_input)
    #city_input.change(fn=city_selected, inputs=city_input, outputs=output)

demo.launch(debug=True)