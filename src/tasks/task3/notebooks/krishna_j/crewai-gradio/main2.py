import gradio as gr
from fpdf import FPDF
import folium
from io import BytesIO
from agents import TravelAgents
from tasks import TravelTasks
from crewai import Crew
from textwrap import dedent
from dotenv import load_dotenv
import geopy
from geopy.geocoders import Nominatim
import os
import json  # Import the json module

load_dotenv()

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        agents = TravelAgents()
        tasks = TravelTasks()

        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent,
            self.cities,
            self.date_range,
            self.interests
        )

        identify_city = tasks.identify_city(
            city_selection_expert,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )

        gather_city_info = tasks.gather_city_info(
            local_tour_guide,
            self.cities,
            self.date_range,
            self.interests
        )

        crew = Crew(
            agents=[expert_travel_agent,
                    city_selection_expert,
                    local_tour_guide],
            tasks=[
                plan_itinerary,
                identify_city,
                gather_city_info
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result

    def generate_map(self):
        geolocator = Nominatim(user_agent="travel_itinerary")
        map = folium.Map(location=[48.8566, 2.3522], zoom_start=12)  # Default to Paris

        attractions = [
            "Eiffel Tower, Paris",
            "Louvre Museum, Paris",
            "Notre-Dame Cathedral, Paris",
            "Montmartre, Paris",
            "Champs-Élysées, Paris",
            "Rodin Museum, Paris",
            "Le Marais, Paris",
            "Palais Garnier, Paris",
            "Centre Pompidou, Paris",
            "Bois de Boulogne, Paris",
            "Luxembourg Gardens, Paris"
        ]

        for attraction in attractions:
            location = geolocator.geocode(attraction)
            if location:
                folium.Marker(
                    location=[location.latitude, location.longitude],
                    popup=attraction
                ).add_to(map)

        map_file = BytesIO()
        map.save(map_file, close_file=False)
        map_file.seek(0)
        return map_file

    def generate_pdf(self, content):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVu", "", os.path.join("fonts", "DejaVuSans.ttf"))
        pdf.set_font("DejaVu", size=12)

        pdf.multi_cell(0, 10, content)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output

def handle_result(result):
    if isinstance(result, dict):
        return result
    elif isinstance(result, str):
        try:
            result_dict = json.loads(result)
            return result_dict
        except json.JSONDecodeError:
            # If it's a plain string, we'll treat it as the final plan text
            return {"final": result}
    else:
        raise ValueError("Unexpected result type from crew.kickoff()")

def generate_trip_plan(origin, cities, date_range, interests):
    trip_crew = TripCrew(origin, cities, date_range, interests)
    result = trip_crew.run()

    # Ensure result is a dictionary
    result = handle_result(result)

    # Extract content for PDF and display
    content = result.get("final", "No final trip plan generated.")

    # Generate the map
    map_file = trip_crew.generate_map()
    pdf_output = trip_crew.generate_pdf(content)

    # Display the map as HTML in Gradio interface
    map_html = map_file.getvalue().decode()

    return content, map_html, pdf_output

iface = gr.Interface(
    fn=generate_trip_plan,
    inputs=[
        gr.Textbox(label="Origin"),
        gr.Textbox(label="Cities (comma separated)"),
        gr.Textbox(label="Date Range"),
        gr.Textbox(label="Interests")
    ],
    outputs=[
        gr.Textbox(label="Trip Plan"),
        gr.HTML(label="Map"),
        gr.File(label="Download PDF", file_count="single")
    ],
    title="Trip Planner Crew",
    description="Generate a 7-day travel itinerary with detailed per-day plans."
)

if __name__ == "__main__":
    iface.launch()