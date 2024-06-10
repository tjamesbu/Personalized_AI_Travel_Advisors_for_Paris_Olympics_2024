##************************************************************************
## using the model "llama3-70b-8192" from chatGroq API. You can change the model name.
## Also experimented with the Mistral model from Huffing face
## There are four agents: 1) information_gatherer, 2) emotional_support ,3)cultural_advisor and 4) safety_advisor
##************************************************************************

import streamlit as st
from crewai import Agent
from langchain_groq import ChatGroq
import os
from langchain_community.llms import HuggingFaceEndpoint
from crewai_tools import SerperDevTool

serper_tool = SerperDevTool(api_key=os.environ["SERPER_API_KEY"])

# using the model from Groq cloud API-- > https://console.groq.com
# need to put the API key in the .env file
llm = ChatGroq(temperature=0.1, groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-70b-8192")

def streamlit_callback(step_output):
    # This function will be called after each step of the agent's execution
    st.markdown("---")
    for step in step_output:
        if isinstance(step, tuple) and len(step) == 2:
            action, observation = step
            if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action:
                st.markdown(f"# Action")
                st.markdown(f"**Tool:** {action['tool']}")
                st.markdown(f"**Tool Input** {action['tool_input']}")
                st.markdown(f"**Log:** {action['log']}")
                st.markdown(f"**Action:** {action['Action']}")
                st.markdown(
                    f"**Action Input:** ```json\n{action['tool_input']}\n```")
            elif isinstance(action, str):
                st.markdown(f"**Action:** {action}")
            else:
                st.markdown(f"**Action:** {str(action)}")

            st.markdown(f"**Observation**")
            if isinstance(observation, str):
                observation_lines = observation.split('\n')
                for line in observation_lines:
                    if line.startswith('Title: '):
                        st.markdown(f"**Title:** {line[7:]}")
                    elif line.startswith('Link: '):
                        st.markdown(f"**Link:** {line[6:]}")
                    elif line.startswith('Snippet: '):
                        st.markdown(f"**Snippet:** {line[9:]}")
                    elif line.startswith('-'):
                        st.markdown(line)
                    else:
                        st.markdown(line)
            else:
                st.markdown(str(observation))
        else:
            st.markdown(step)

class ParisSyndromeAdvisor():

  def information_gatherer(self):
    return Agent(
      role='Website scraper',
      goal='Scrape the contents of the website URLs',
      backstory="""An efficient information extractor who gathers the relevant information""",
      verbose=True,
      llm=llm,
      allow_delegation=False,
      step_callback = streamlit_callback
    )

  def emotional_support(self):
    return Agent(
        role='Mental Health Specialist',
        goal='Provide mental health advice to the travelers suffering from Paris Syndrome',
        backstory="""A specialist who has knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods""",
        tools = [serper_tool],
        verbose=True,
        llm=llm,
        max_iter = 5,
        allow_delegation=False,
        step_callback = streamlit_callback
    )

  def cultural_advisor(self):
    return Agent(
        role='Specialist Cultural Advisor',
        goal='Educate the user about cultural differences and help them adjust their expectations',
        backstory="""An expert in French culture and customs, dedicated to helping travelers understand and appreciate cultural differences to reduce cultural shock.""",
        tools = [serper_tool],
        verbose=True,
        llm=llm,
        max_iter = 5,
        allow_delegation=False,
        step_callback=streamlit_callback
    )

  def safety_advisor(self):
    return Agent(
      role='Safety Advisor',
      goal='Educate the users about the unsafe places and provide them with relevant safety tips and guidelines',
      backstory="""An expert who has an extensive knowledge on the unsafe areas and provide the necessary safety guidelines""",
      tools = [serper_tool],
      verbose = True,
      llm=llm,
      max_iter= 5,
      allow_delegation = False,
      step_callback = streamlit_callback
    )