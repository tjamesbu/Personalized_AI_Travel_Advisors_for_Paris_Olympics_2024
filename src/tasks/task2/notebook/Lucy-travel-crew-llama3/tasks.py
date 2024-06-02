from crewai import Task
from textwrap import dedent

from tools import search_hotels, open_page

class TravelTasks():

  def recommend(self, agent, interests, days):
    return Task(
      description=(
        "1. Recommend local attractions for a visitor according to their"
            "{interests}. Prioritize lesser known attractions that are away from tourist crowds."
        "2. Recommend authentic Parisian experiences according to "
            "visitor's {interests}."
        "3. Recommend authentic local restaurants. "
        "4. Recommend enough attractions to fill {days} days with activities in the mornings and afternoons."
        "4. Recommend enough places to eat for {days} days for breakfast, lunch and dinner."
        "5. Recommend public transportation near every place on your list."
      ),
      expected_output="""A list of items, where each item includes the name of a place in Paris, location of the place, public transportation nearby and a short description of why this place is worth visiting""",
      agent=agent,
      )

  def find_hotel(self, agent):
    return Task(
      description=(
        "1. Recommend hotels in Central Paris, France to a visitor."
        "2. Your recommendations must be divided into 3 groups according to price per night:"
        "less than $200/per night, $200 - $500/ per night and above $500 per night."
        "3. Each group must contain 5 recommended hotels."
        "4. Only recommend the hotels with rating 8.0 and above."
      ),
      expected_output="""A list of 3 groups of hotels, grouped by the price per night. Each group must contain 5 recommendations. For each hotel give the name and address.""",
      tools=[search_hotels, open_page],
      agent=agent
      )

  def plan(self, agent, interests, days):
    return Task(
      description = (
        "2. Present the recommendations of the Paris tour guide as a full {days}-day travel plan."
        "4. You MUST give public transportation nearb each attraction, restaurant or event in the suggested travel plan."
        "3. Append the hotel recommendations of the hotel guide at the bottom of the travel itinerary."
      ),
      expected_output = """Your final answer MUST be a complete day-by-day travel plan, based on the output of the recommend task formatted as markdown, displaying daily recommendations that include:
              1. At least two places to visit each day
              2. Restaurants to eat breakfast, lunch and dinner
              3. Public transportation near each place
              4. The reason you picked each place, what makes them special
      At the bottom append the hotel recommendations given by the hotel guide.""",
      agent=agent,
      )   
  
 