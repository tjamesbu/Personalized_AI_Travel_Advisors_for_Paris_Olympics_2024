##***********************************************************************************
## Gradio application for the Paris syndrome advisor using crew ai
## Contributor: N Priyanka
## Date: 28th May 2024
##***********************************************************************************

import os
from crewai import Crew
from advisor_agents import ParisSyndromeAdvisor
from advisor_tasks import AdvisorTasks
import gradio as gr

from dotenv import load_dotenv
load_dotenv()

class AdvisorCrew:
    def __init__(self, origin, destination, interests, questions):
        self.origin = origin
        self.destination = destination
        self.interests = interests
        self.questions = questions
        self.answers = {}

    def ask_questions(self):
        for key, question in self.questions:
            self.answers[key] = ""
        return self.questions

    def get_answers(self, answers):
        self.answers = {key: value for (key, _), value in zip(self.questions, answers)}
        return self.answers

    def run(self):
        agents = ParisSyndromeAdvisor()
        tasks = AdvisorTasks()

        syndrome_advisor_agent = agents.emotional_support()
        cultural_advisor_agent = agents.cultural_advisor()

        support_task = tasks.support_task(
            syndrome_advisor_agent,
            self.origin,
            self.destination,
            list(self.answers.values()),
        )
        advisor_task = tasks.cultural_task(
            cultural_advisor_agent,
            self.origin,
            self.destination,
            self.interests,
        )

        crew = Crew(
            agents=[syndrome_advisor_agent, cultural_advisor_agent],
            tasks=[support_task, advisor_task],
            full_output=True,
            verbose=2,
            output_log_file=True,
        )

        result = crew.kickoff()
        return result

questions = [
        ("expectations", "What were your expectations of Paris before you arrived? Were there specific places or experiences you were looking forward to in Paris?"),
        ("experiences", "How have your experiences in Paris differed from your expectations? Can you describe specific incidents or aspects of Paris that have been disappointing or distressing?"),
        ("emotional_state", "How are you feeling emotionally and mentally during your visit to Paris? Have you experienced symptoms like anxiety, depression, or disorientation since arriving in Paris?"),
        ("social_interactions", "How have your interactions with locals and other tourists been? Have you faced any language barriers or cultural misunderstandings?"),
        ("coping_strategies", "How are you currently coping with your feelings of disappointment or distress? Are there any activities or places in Paris that have helped improve your mood or alleviate stress?"),
        ("support_systems", "Do you have friends, family, or acquaintances in Paris you can talk to about your feelings? Are you in contact with any mental health professionals or support groups?"),
        ("duration", "How long do you plan to stay in Paris? Do you have any flexibility in your travel plans to visit other places or change your itinerary?"),
        ("health_safety", "Have you sought any medical or psychological assistance since experiencing these feelings? Do you feel safe and secure in your current accommodation and surroundings?"),
        ("reflection", "Looking back, is there anything you think could have prepared you better for this trip? What advice would you give to someone planning a trip to Paris to help them set realistic expectations?"),
        ("personal_background", "Is this your first time traveling abroad, or have you had similar experiences in other destinations? Can you share a bit about your general travel preferences and past travel experiences?"),
    ]

def process_form(origin, destination, interests, *answers):
    
    advisor_crew = AdvisorCrew(origin, destination, interests, questions)
    advisor_crew.get_answers(answers)
    
    # Check if at least 6 answers are non-empty
    count_non_empty = sum(1 for value in answers if value)
    if count_non_empty >= 6:
        result = advisor_crew.run()
        task_outputs = result.get('tasks_outputs', [])
        advice = []
        headers = ['Mental Health Advice', 'Cultural Awareness']
        for header, task_output in zip(headers, task_outputs):
            advice.append(f"**{header}**: {task_output.raw_output}")
        return "\n\n".join(advice)
    else:
        return "Please provide at least 9 responses to the questions."

iface = gr.Interface(
    fn=process_form,
    inputs=[
        gr.Textbox(label="Where are you from?", placeholder="Enter your origin"),
        gr.Textbox(label="Where are you currently in Paris?", placeholder="Enter your destination"),
        gr.Textbox(label="What are your interests?", placeholder="Enter your interests"),
        *[gr.Textbox(label=question, placeholder=f"Answer for {question}") for _, question in questions]
    ],
    outputs="markdown",
    title="👨‍⚕️ Mental Health and Cultural Advisor",
    description="Answer the questions to get advice on mental health and cultural awareness for your trip to Paris.",
    
)

iface.launch()
