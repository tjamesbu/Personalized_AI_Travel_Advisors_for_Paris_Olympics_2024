from crewai import Agent
#from langchain.llms import OpenAI

from langchain_groq import ChatGroq
import os


llm = ChatGroq(temperature=0.0, groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-70b-8192")

class TravelAgents():

  def local_guide(self):
    return Agent(
      role="Paris tour guide",
      goal="""Recommend local attractions         including 'hidden gems' and local experiences to a visitor according to their {interests}, avoid overcrowded tourist areas""",
      backstory = """You have an extensive knowledge of Paris attractions and can give visitors detailed recommendations of places to visit taking their {interests} into consideration. Your recommendations always include lesser known attractions ('hidden gems') that allow the visitors to avoid crowded toursit areas and experience the authentic side of Paris.""",
      allow_delegation=False,
      max_iter=5,
      llm=llm,
	    verbose=True
    )
  
  def hotel_guide(self):
    return Agent(
      role="Expert on finding best hotels in central Paris, France",
      goal="Suggest best hotels for a visitor in Paris, France",
      backstory="""You have an extensive knowledge of hotels in central Paris and can give best hotel recommendations to a visitor according to their budget.""",
      allow_delegation=False,
      max_iter=5,
      llm=llm,
      verbose=True
)
  
  def travel_planner(self): 
    return Agent(
        role="Amazing travel planner",
        goal="""Create travel itineraries for travellers to Paris for {days} days including the best 'hidden gems' attractions and public transportation near each of them.""",
        backstory="""You are a specialist in travel planning with decades of experience. You provide a detailed travel itinerary for number of {days} days, that includes the recommendations of the Paris tour guide""",
        max_iter=5,
        llm=llm,
        verbose=True)