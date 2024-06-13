import os
import time
import httpx
from crewai import Crew
from textwrap import dedent
from langchain_groq import ChatGroq
from advisor_agents import ParisSyndromeAdvisor
from advisor_tasks import AdvisorTasks
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_icon="👨‍⚕️", layout="wide")

class AdvisorCrew:

    def __init__(self, origin, destination, interests, questions):
        self.origin = origin
        self.destination = destination
        self.interests = interests
        self.questions = questions

    def ask_questions(self):
        if 'answers' not in st.session_state:
            st.session_state.answers = []
        if 'question_index' not in st.session_state:
            st.session_state.question_index = 0

        index = st.session_state.question_index
        if index < len(self.questions):
            key, question = self.questions[index]
            st.write("**Answer atleast six questions out of the ten questions to proceed. Click on the Next button to proceed to next question.**")
            if isinstance(question, str):
                with st.chat_message("assistant"):
                    st.write(question)
                with st.chat_message("user"):
                    answer = st.text_area("Your response:", key=f"response_{index}")

                if st.button("Next", key=f"next_{index}"):
                    if answer:
                        st.session_state.answers.append((key, answer))
                        st.session_state.question_index += 1
                        st.rerun()
                    else:
                        st.warning("Please provide an answer before proceeding.")
            else:
                st.warning("Invalid question format. Skipping question.")
                st.session_state.question_index += 1
                st.rerun()
        else:
            st.write("All questions have been answered.")
            st.session_state.all_answers_collected = True
    
    def get_answers(self):
        return st.session_state.answers

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
                st.session_state.answers,
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
                verbose=2,
                output_log_file=True,
            )

            result = crew.kickoff()
            return result
        except httpx.RemoteProtocolError as e:
            st.error("There was a problem with the network connection. Please try again later.")
            st.error(f"Error details: {e}")
            return None
        except Exception as e:
            st.error("An agent stopped due to iteration limit or time limit.")
            st.error(f"Error details: {e}")
            return None

# Function to initialize LLM 
def initialize_llm():
    llm = ChatGroq(temperature=0.1, groq_api_key=os.environ["GROQ_API_KEY"], model_name="llama3-70b-8192")

    return llm

def generate_welcome_message(llm):
    prompt = """
    You are an AI assistant designed to welcome users to the "Paris Syndrome Advisor" app, which helps travelers to Paris manage their expectations and symptoms. Your task is to greet the user with an appealing welcome message and then prompt them to provide their query or concern. Follow these steps:

    1. Start with a warm and friendly welcome message.
    2. Briefly explain what the "Paris Syndrome Advisor" app does. 
    3. Invite the user to share their questions or concerns about traveling to Paris.

    The app provides the travelers with mental health recommendations, cultural awareness and safety tips.

    Here is an example format you can follow:

    ---

    **Welcome Message Example:**

    "Bonjour and welcome to the Paris Syndrome Advisor app! 🌟 

    Are you excited about your upcoming trip to Paris but feeling a bit anxious or unsure? Don't worry, you've come to the right place! Our app is here to help you manage your expectations. Whether you're concerned about paris syndrome, cultural differences, or safety tips and emergency contacts, we're here to help.

    Please tell us about your questions or concerns, and let's make your Paris adventure as wonderful as possible!"

    ---

    """

    response = llm.invoke(prompt)
    message_text = response.content
    # Split the message into lines
    lines = message_text.split(" ")

    # Yield each line of the message
    for line in lines:
        yield line + " "
        time.sleep(0.02)
    

def main():
    st.markdown("<h1 style='text-align: center;'>🧠👮‍♂️ Paris Syndrome Psychiatry Advisor </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'> Welcome to Paris Mental Health, Safety and Cultural Advisor! </h3>", unsafe_allow_html=True)

    if "initial_user_query" not in st.session_state:
        st.session_state["initial_user_query"] = ""
    if "initial_processing_done" not in st.session_state:
        st.session_state["initial_processing_done"] = False
    if 'origin' not in st.session_state:
        st.session_state.origin = ""
    if 'destination' not in st.session_state:
        st.session_state.destination = ""
    if 'interests' not in st.session_state:
        st.session_state.interests = ""
    if 'all_answers_collected' not in st.session_state:
        st.session_state.all_answers_collected = False

    # Check if the welcome message has already been displayed
    if "welcome_message_displayed" not in st.session_state:
    #Generate Welcome Message with User Input
        with st.chat_message("assistant"):
            llm = initialize_llm()
            # Display the message as a streaming message
            st.write_stream(generate_welcome_message(llm))
            st.session_state["welcome_message_displayed"] = True

    if not st.session_state["initial_user_query"]:
        with st.chat_message("user"):
            query = st.chat_input("Enter your question")        

            if query:
                st.session_state["initial_user_query"] = query
                st.rerun()  
                
    if st.session_state["initial_user_query"] and not st.session_state["initial_processing_done"]:
        with st.spinner("Processing..."):
            time.sleep(2)
        
        st.session_state["initial_processing_done"] = True
        st.rerun()
    
    # Display input fields after the initial processing is done
    if st.session_state["initial_processing_done"]:
        with st.chat_message("assistant"):
            st.write("Answer the below questions to help address your concerns and provide you relevant recommendations and suggestions.")
        
        st.header("👇 Enter your trip details")
        
        st.session_state.origin = st.text_input("Where are you from?", value=st.session_state.origin, help="Required field")
        st.session_state.destination = st.text_input("Where are you currently in Paris?", value=st.session_state.destination, help="Required field")
        st.session_state.interests = st.text_area("What are your interests?", value=st.session_state.interests, help="Required field")

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

        advisor_crew = AdvisorCrew(st.session_state.origin, st.session_state.destination, st.session_state.interests, questions)

        if not st.session_state.all_answers_collected:
            advisor_crew.ask_questions()
        else:
            st.write("You have completed all the questions. Please submit your answers.")
        
        answers = advisor_crew.get_answers()
        count_non_empty = sum(1 for key, value in answers if value)
        
        submitted = st.button("**Submit**")

        if submitted and all([st.session_state.origin, st.session_state.destination, st.session_state.interests]) and count_non_empty >= 6:
            st.write("Thank you for your input. I will process your query and generate the results.")
            with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
                with st.container(height=500, border=False):
                    result = advisor_crew.run()
                status.update(label="✅ Advice is ready!", state="complete", expanded=False)

            st.subheader("Here is the advice")

            col1, col2 = st.columns(2)

            task_outputs = result.get('tasks_outputs', [])
            headers = ['Emergency Contact Information', 'Mental Health Advice', 'Cultural Awareness', 'Safety Guidelines']
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

        elif submitted and count_non_empty<6 and all([st.session_state.origin, st.session_state.destination, st.session_state.interests]):
            st.info("Kindly answer atleast 6 questions")
        elif submitted and count_non_empty<=6 and not all([st.session_state.origin, st.session_state.destination, st.session_state.interests]):
            st.info("Enter the required fields")
        elif submitted or count_non_empty<=6 or not all([st.session_state.origin, st.session_state.destination, st.session_state.interests]):
            st.info("Answer the questions to proceed")

if __name__ == "__main__":
    main()
