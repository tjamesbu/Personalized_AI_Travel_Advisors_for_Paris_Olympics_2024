##************************************************************************
## using the model "llama3-70b-8192" from chatGroq API. You can change the model name.
## Also experimented with the Mistral model from Huffing face
## There are two agents: 1) emotional_support and 2) cultural_advisor
##************************************************************************

from crewai import Agent
#from langchain.llms import OpenAI
from langchain_groq import ChatGroq
import os
from langchain_community.llms import HuggingFaceEndpoint


# using the model from Groq cloud API-- > https://console.groq.com
# need to put the API key in the .env file
llm = ChatGroq(temperature=0.1, groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-70b-8192")

## Using the model from Hugging Face. You can try with different models changing the repo_id.
#repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

# llm = HuggingFaceEndpoint(
#     repo_id=repo_id, temperature=0.2,
#     max_new_tokens=512,
#     huggingfacehub_api_token=os.environ["HF_TOKEN"]
# )

class ParisSyndromeAdvisor():

  def emotional_support(self):
    return Agent(
        role='Mental Health Advisor',
        goal='Provide mental health advice to the travelers suffering from Paris Syndrome',
        backstory="""A specialist who has knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods""",
        verbose=True,
        llm=llm,
        allow_delegation=False
    )

  def cultural_advisor(self):
    return Agent(
        role='Cultural Advisor',
        goal='Educate the user about cultural differences and help them adjust their expectations',
        backstory="""An expert in French culture and customs, dedicated to helping travelers understand and appreciate cultural differences to reduce cultural shock.""",
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
