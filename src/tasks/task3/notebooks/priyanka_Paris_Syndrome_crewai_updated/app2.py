##*******************************************************************************************
##**Contributor: N Priyanka**
## **Date: 7th June 2024**
## This implements the crew for Paris syndrome mental health advisor. The crew has four agents
## These agents advice on the mental health, provides safety advice and cultural awareness to the travelers.
## 
##********************************************************************************************

import os
from crewai import Crew
from textwrap import dedent
from advisor_agents import ParisSyndromeAdvisor
from advisor_tasks import AdvisorTasks
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_icon="👨‍⚕️", layout="wide")

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
        self.answers = []  # Clear previous answers if any
        for key, question in self.questions:
            if isinstance(question, str):
                answer = st.text_area(question + " ")

                self.answers.append((key,answer))
            else:
                print("Invalid question format. Skipping question.",key)

    def get_answers(self):
        return self.answers
 
    def run(self):
        try:
            agents = ParisSyndromeAdvisor()
            tasks = AdvisorTasks()

            information_gatherer = agents.information_gatherer()
            syndrome_advisor_agent = agents.emotional_support()
            cultural_advisor_agent = agents.cultural_advisor()
            safety_advisor_agent = agents.safety_advisor()
            
            gather_task = tasks.gather_task(
            information_gatherer,
            self.origin,
            self.destination,
            )

            support_task = tasks.support_task(
            syndrome_advisor_agent,
            self.origin,
            self.destination,
            # self.problem,
            self.answers,
            gather_task
            )

            advisor_task = tasks.cultural_task(
            cultural_advisor_agent,
            self.origin,
            self.destination,
            # self.problem,
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
            verbose=2,
            output_log_file=True,
            )

            result = crew.kickoff()
            return result
        except httpx.RemoteProtocolError as e:
            st.error("There was a problem with the network connection. Please try again later.")
            st.error(f"Error details: {e}")
            return None

def main():
    st.title("👨‍⚕️ Mental Health and Cultural Advisor")
    
    st.subheader("Welcome to Paris Mental Health and Cultural Advisor!",
                 divider="rainbow", anchor=False)
    st.markdown("Answer the questions in the sidebar to proceed.")

    
    with st.sidebar:
        st.header("👇 Enter your trip details")
        with st.sidebar:
            origin = st.text_input("Where are you from?")
                
            destination = st.text_input("Where are you currently in Paris?")
                
            interests = st.text_area("What are your interests?")
            
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
            # Count the number of tuples with non-empty second elements
            count_non_empty = sum(1 for key, value in answers if value)

            
    # Check if any user input is empty before setting submitted
    submitted = st.button("**Submit**")
    
    if submitted and all([origin, destination, interests]) and count_non_empty >= 6:
        
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                result = advisor_crew.run()
            status.update(label="✅ Advice is ready!",
                        state="complete", expanded=False)

        st.subheader("Here is the advice", anchor=False, divider="rainbow")
        
        col1, col2 = st.columns(2)

        task_outputs = result.get('tasks_outputs', [])
        headers = ['Emergency Contact Information','Mental Health Advice','Cultural Awareness','Safety Guidelines']
        # Loop through each TaskOutput and display information
        for header, task_output in zip(headers, task_outputs):
            with st.expander(header):
                if header == "Emergency Contact Information":
                    with col1:
                        st.subheader("Emergency contacts")
                        st.write(f"{task_output.raw_output}")
                elif header == "Safety Guidelines":
                    with col2:
                        st.subheader("Safety guidelines")
                        st.write(f"{task_output.raw_output}")
                else:
                    st.write(f"{task_output.raw_output}")
    
if __name__=="__main__":
    main()
        
        
                