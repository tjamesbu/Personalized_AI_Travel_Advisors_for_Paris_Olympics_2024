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

#tool used
serper_tool = SerperDevTool(api_key=os.environ["SERPER_API_KEY"])

# using the model from Groq cloud API-- > https://console.groq.com
# need to put the API key in the .env file
llm = ChatGroq(temperature=0.1, groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-70b-8192")

class ParisSyndromeAdvisor():

  def information_gatherer(self):
    return Agent(
      role='Website scraper',
      goal='Scrape the contents of the webiste URLs',
      backstory="""An efficient information extractor who gathers the relevant information""",
      verbose=True,
      llm=llm,
      allow_delegation=False
    )

  def emotional_support(self):
    return Agent(
        role='Mental Health Specialist',
        goal='Provide mental health advice to the travelers suffering from Paris Syndrome',
        backstory="""A specialist who has knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods""",
        tools = [serper_tool],
        verbose=True,
        llm=llm,
        max_rpm = 2,
        allow_delegation=False,
        
    )

  def cultural_advisor(self):
    return Agent(
        role='Specialist Cultural Advisor',
        goal='Educate the user about cultural differences and help them adjust their expectations',
        backstory="""An expert in French culture and customs, dedicated to helping travelers understand and appreciate cultural differences to reduce cultural shock.""",
        tools = [serper_tool],
        verbose=True,
        llm=llm,
        max_rpm = 2,
        allow_delegation=False,
        
    )

  def safety_advisor(self):
    return Agent(
      role='Safety Advisor',
      goal='Educate the users about the unsafe places and provide them with relevant safety tips and guidelines',
      backstory="""An expert who has an extensive knowledge on the unsafe areas and provide the necessary safety guidelines""",
      tools = [serper_tool],
      verbose = True,
      llm=llm,
      max_rpm = 2,
    )