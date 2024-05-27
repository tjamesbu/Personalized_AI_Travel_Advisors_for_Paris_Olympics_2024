from crewai import Agent, Task, Crew, Process
from crewai.tasks.task_output import TaskOutput
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()


llm_client = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0.1)


search = TavilySearchAPIWrapper()
search_tool = TavilySearchResults(api_wrapper=search)

class WebSearchCrew():

    def search_result_callback(self, output: TaskOutput):
        if output.result is not None:
            print("\n\n[Tavilly] Search task completed successfully!")
            #print("Search Results:\n", output.result)
        else:
            print("\n\n[Tavilly] Search task failed to produce output.")


    def __init__(self, research_topic):
        # Define agents with specific roles and tools
        researcher = Agent(
            role='Information Researcher',
            goal=f'Search the internet for the latest news , announcement about {research_topic} with accurate sourcing.',
            backstory="""As a Researcher, passionate about technology industry's forefront, you meticulously gather and verify the latest business trend and products developments. Your quest for truth requires verifying the authenticity of information, ensuring a credible knowledge base for informed decision-making.""",
            verbose=False,
            llm=llm_client
        )

        # Create tasks for the agents
        research_task = Task(
            description=f'Search 3 topic for {research_topic}, ensuring all data is backed by credible sources. Compile a report detailing each finding and its source for verification.', 
            expected_output=f'Summary of 3 latest news on {research_topic} with credible sources.',
            tools=[search_tool], 
            agent=researcher,
            callback=self.search_result_callback
        )

        # Assemble the crew with a sequential process
        self.search_crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            process=Process.sequential,
            verbose=False,
        )

    def search(self):
        result = self.search_crew.kickoff()
        return result

if __name__ == '__main__':
    # Start the crew's task execution
    my_crew = WebSearchCrew("best museum in Paris")
    result = my_crew.search()
    print(result)