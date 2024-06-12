from llm.llm_factory import get_llm
from crewai import Crew
from crew.web_search_crew.websearch_crew import WebSearchCrew

llm = get_llm()

def get_crew(crew_name:str, **kwargs) -> Crew:
    match crew_name:
        case 'WebSearchCrew':
            crew = WebSearchCrew(llm=llm, research_topic=kwargs['research_topic'])
        case 'LocalAttractionCrew':
            # Add code to get crew and return it
            pass
        case _:
            raise ValueError
    return crew


if __name__ == '__main__':
    # Example code
    my_crew = get_crew(crew_name='WebSearchCrew', research_topic='Best retaurant in Paris')
    response = my_crew.kickoff()
    print(response)