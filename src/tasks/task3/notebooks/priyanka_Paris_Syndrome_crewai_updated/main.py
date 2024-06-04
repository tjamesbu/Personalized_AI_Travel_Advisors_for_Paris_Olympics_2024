##*******************************************************************************************
##**Contributor: N Priyanka**
## **Date: 24th May 2024**
## This implements the crew for Paris syndrome mental health advisor. The crew has two agents
## One for advising on mental health condition and another one for cultural awareness
## 
##********************************************************************************************

import os
from crewai import Crew, Process
from textwrap import dedent
from advisor_agents import ParisSyndromeAdvisor
from advisor_tasks import AdvisorTasks
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

class AdvisorCrew:

  def __init__(self, origin, destination, interests , questions):
    self.origin = origin
    self.destination = destination
    self.interests = interests
    # self.problem = problem
    self.questions = questions
    self.answers = []


  def ask_questions(self):
    print("Please answer the following questions:")
    for key, question in self.questions:
        if isinstance(question, str):
          answer = input(question + " ")
          self.answers.append((key,answer))
        else:
          print("Invalid question format. Skipping question.",key)

  def get_answers(self):
    return self.answers

  def run(self):
    agents = ParisSyndromeAdvisor()
    tasks = AdvisorTasks()

    information_gatherer = agents.information_gatherer()
    syndrome_advisor_agent = agents.emotional_support()
    cultural_advisor_agent = agents.cultural_advisor()
    safety_advisor_agent = agents.safety_advisor()
    
    llm = ChatGroq(temperature=0.1, groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-70b-8192")

    gather_task = tasks.gather_task(
      information_gatherer,
      self.origin,
      self.destination,
    )

    support_task = tasks.support_task(
      syndrome_advisor_agent,
      self.origin,
      self.destination,
      self.answers,
      gather_task
    )
    advisor_task = tasks.cultural_task(
      cultural_advisor_agent,
      self.origin,
      self.destination,
      self.interests,
      support_task
    )

    safety_advisor_task = tasks.safety_advisor_task(
      safety_advisor_agent,
      self.destination,
      gather_task,
    )
    
    crew = Crew(
      agents=[
        information_gatherer, syndrome_advisor_agent, cultural_advisor_agent, safety_advisor_agent
      ],
      tasks=[gather_task, support_task, advisor_task, safety_advisor_task],
      full_output=True,
      process = Process.sequential,
      verbose=2,
      # manager_llm = llm,
      output_log_file=True,
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  
  print("## Welcome to Trip Planner Crew")
  print('-------------------------------')
  origin = input(
    dedent("""
      Where are you from?
    """))
  destination = input(
    dedent("""
      Where are you currently in Paris?
    """))
  interests = input(
    dedent("""
      What are your interests?
      """))
  # problem = input(
  #   dedent("""
  #   Tell me about your problems.
  #   """))
  questions = [
            ("expectations","What were your expectations of Paris before you arrived? Were there specific places or experiences you were looking forward to in Paris?"),
            ("experiences","How have your experiences in Paris differed from your expectations? Can you describe specific incidents or aspects of Paris that have been disappointing or distressing?"),
            ("emotional_state","How are you feeling emotionally and mentally during your visit to Paris? Have you experienced symptoms like anxiety, depression, or disorientation since arriving in Paris?"),
            ("social_interactions","How have your interactions with locals and other tourists been? Have you faced any language barriers or cultural misunderstandings?"),
            ("coping_strategies","How are you currently coping with your feelings of disappointment or distress? Are there any activities or places in Paris that have helped improve your mood or alleviate stress?"),
            ("support_systems","Do you have friends, family, or acquaintances in Paris you can talk to about your feelings? Are you in contact with any mental health professionals or support groups?"),
            ("duration","How long do you plan to stay in Paris? Do you have any flexibility in your travel plans to visit other places or change your itinerary?"),
            ("health_safety","Have you sought any medical or psychological assistance since experiencing these feelings? Do you feel safe and secure in your current accommodation and surroundings?"),
            ("reflection","Looking back, is there anything you think could have prepared you better for this trip? What advice would you give to someone planning a trip to Paris to help them set realistic expectations?"),
            ("personal_background","Is this your first time traveling abroad, or have you had similar experiences in other destinations? Can you share a bit about your general travel preferences and past travel experiences?"),
           
        ]
  
    
  advisor_crew = AdvisorCrew(origin, destination, interests, questions)
  advisor_crew.ask_questions()
  answers = advisor_crew.get_answers()
  result = advisor_crew.run()
  #task_outputs = result.get('tasks_outputs', [])
  # result = result['final_output']
  print("\n\n########################")
  print("## Here is the advice")
  print("########################\n")
  print(result)

  # # Save the response to a text file
  # filepath = "response_1.txt"
  # with open(filepath, "w", encoding="utf-8") as f:
  #   f.write(result)
