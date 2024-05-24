##*********************************************************************
##There are two tasks: 1) support_task and 2)cultural_task
##********************************************************************

from crewai import Task
from textwrap import dedent
from datetime import date

class AdvisorTasks():

    def support_task(self, agent, origin, destination, answers):
        return Task(
            description=dedent(f"""
                I will provide you with an individual looking for guidance and advice on managing their emotions, stress, anxiety and other mental health issues arising due to Paris syndrome. 
                Use your knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods in order to create strategies that the individual can implement in order to improve their overall wellbeing.
                Use the {answers} to provide the best advice. 
                
                Origin: {origin}
                Destination: {destination}
                Answers: {answers}
                """),
            expected_output=dedent("""
                A summary of the conversation highlighting:
                1. Key concerns expressed by the user.
                2. Emotional reassurance provided.
                3. Recommended coping strategies.
                4. Also, recommend any mental helplines in the {destination} if you have the correct information. Otherwise, do not provide any fake numbers.
                """),
            agent=agent,
            
        )

    def cultural_task(self, agent, origin, destination, interests):
        return Task(
            description=dedent(f"""
                Educate the user about cultural differences and customs in {destination}.
                Provide tips on local etiquette and practices to help them adjust their expectations and also help address their problems.
                
                Origin: {origin}
                Destination: {destination}
                Interests: {interests}
                
                """),
            expected_output=dedent("""
                A cultural guide that includes:
                1. Key cultural differences to be aware of.
                2. Local etiquette and customs.
                3. Tips for blending in and avoiding cultural misunderstandings.
                4. Recommendations for culturally immersive experiences based on the user's interests.
                """),
            agent=agent
        )


