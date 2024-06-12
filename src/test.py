from crew_factory import get_crew

my_crew = get_crew(crew_name='WebSearchCrew', research_topic='Best retaurant in Paris')
response = my_crew.kickoff()
print(response)