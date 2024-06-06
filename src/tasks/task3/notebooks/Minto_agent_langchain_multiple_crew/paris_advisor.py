from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from textwrap import dedent
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4o', temperature=0.1)

class ParisAdvisor:
        
    def reset(self) -> None:        
        self.answers = []
        self.qa_in_progress = False
        self.session_in_progress = False
        self.current_question = 0

    def __init__(self) -> None:
        self.questions = [
            "What were your expectations of Paris before you arrived? Were there specific places or experiences you were looking forward to in Paris?",
            "How have your experiences in Paris differed from your expectations? Can you describe specific incidents or aspects of Paris that have been disappointing or distressing?",
            "How are you feeling emotionally and mentally during your visit to Paris? Have you experienced symptoms like anxiety, depression, or disorientation since arriving in Paris?",
            "How have your interactions with locals and other tourists been? Have you faced any language barriers or cultural misunderstandings?",
            "How are you currently coping with your feelings of disappointment or distress? Are there any activities or places in Paris that have helped improve your mood or alleviate stress?",
            "Do you have friends, family, or acquaintances in Paris you can talk to about your feelings? Are you in contact with any mental health professionals or support groups?",
            "How long do you plan to stay in Paris? Do you have any flexibility in your travel plans to visit other places or change your itinerary?",
            "Have you sought any medical or psychological assistance since experiencing these feelings? Do you feel safe and secure in your current accommodation and surroundings?",
            "Looking back, is there anything you think could have prepared you better for this trip? What advice would you give to someone planning a trip to Paris to help them set realistic expectations?",
            "Is this your first time traveling abroad, or have you had similar experiences in other destinations? Can you share a bit about your general travel preferences and past travel experiences?",
        ]
        self.reset()
    
    def get_questions(self) -> list[str]:
        return self.questions
        
    def start_session(self) -> None:
        self.session_in_progress = True
        self.qa_in_progress = True
        self.current_question = 0
        
    def save_answer(self, answer) -> None:
        self.answers.append(answer)
    
    def get_next_question(self) -> str:
        question = self.questions[self.current_question]
        self.current_question += 1
        if self.current_question == len(self.questions):
            self.qa_in_progress = False
        return question
    
    def has_more_questions(self) -> bool:
        return self.qa_in_progress
    
    def is_session_in_progress(self) -> bool:
        return self.session_in_progress

    def summarize(self) -> str:
        text_content = ""

        for q, a in zip(self.questions, self.answers):
            text_content += f"Q: {q}\nA: {a}\n\n"

        # Remove the last extra newline character
        text_content = text_content.strip()
        return text_content
    
    # Reused from Priyanka's code
    def get_recommendation(self) -> str:
        self.emotional_support_agent= Agent(
            role='Mental Health Advisor',
            goal='Provide mental health advice to the travelers suffering from Paris Syndrome',
            backstory="""A specialist who has knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods""",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

        support_task = Task(
            description=dedent(f"""
                You are an intelligent AI assistant for supporting the visitors to the city of Paris.
                I will provide you with an individual looking for guidance and advice on managing their emotions, stress, anxiety and other mental health issues arising due to Paris syndrome. 
                Use your knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods in order to provide a brief recommendation that the individual can implement in order to improve their overall wellbeing.
                Refer the below questions and answers to provide the best advice. 
                
                {self.summarize()}
                """),
            expected_output=dedent("""
                Greet the user warmly and acknowledge their distress, reassuring them that their feelings are valid and common. 
                Provide a brief explanation of your understanding of user's problem, 
                and suggest immediate self-care actions as well as coping strategies. 
                Encourage them to reach out again if their symptoms persist.
                Use second person pronoun to address the user.
                """),
            agent=self.emotional_support_agent            
        )

        crew = Crew(
            agents=[self.emotional_support_agent],
            tasks=[support_task],
            verbose=2,
            output_log_file=True,
        )

        result = crew.kickoff()
        self.reset()
        return result
    



if __name__ == '__main__':
    advisor = ParisAdvisor()
    while (advisor.has_more_questions()):
        print(f'Q: {advisor.get_next_question()}')
        answer = input('A: ')
        advisor.save_answer(answer)
        print('----')
    print('======================================================')
    print(advisor.get_recommendation())
    print('======================================================')