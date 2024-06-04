import json
import unidecode
import gradio as gr
from difflib import get_close_matches

# Load and preprocess city data from JSON
def load_and_preprocess_city_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        city_data = json.load(file)
    for city in city_data:
        city['name'] = unidecode.unidecode(city['name'])
    return city_data

city_data = load_and_preprocess_city_data('world_cities_(including_all_states_and_counties).json')

# Function to get city suggestions
def get_city_suggestions(query):
    if not query:
        return []
    query = unidecode.unidecode(query).lower()
    city_list = [f"{city['name']}, {city['state']}, {city['country']}" for city in city_data]
    matches = get_close_matches(query, city_list, n=5, cutoff=0.1)
    return matches

# Function to handle city selection
def city_selected(city_name):
    return f"Selected City: {city_name}"

# Gradio interface
with gr.Blocks() as demo:
    city_input = gr.Textbox(label="Type a city")
    suggestions = gr.Dropdown(label="Select a city", interactive=True)
    output = gr.Textbox(label="Output")
    
    city_input.change(fn=lambda x: gr.update(choices=get_city_suggestions(x)), inputs=city_input, outputs=suggestions)
    suggestions.change(fn=city_selected, inputs=suggestions, outputs=output)

demo.launch(debug=True)