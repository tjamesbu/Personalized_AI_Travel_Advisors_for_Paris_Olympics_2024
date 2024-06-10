##*********************************************************************
##There are four tasks: 1) gather_task, 2) support_task, 3)cultural_task and 4)safety_advisor_task
##********************************************************************

from crewai import Task
from textwrap import dedent
from datetime import date

class AdvisorTasks():

    def gather_task(self, agent, origin, destination):
        return Task(
            description=dedent(f"""
            I want you to act as a web scraper who scrapes the website content given the following URLs
            and extracts the relevant information required by the agents.
            URLs = "https://findahelpline.com/countries/fr,
                    https://soshelpline.org/mental-health-resources/,
                    https://embassies.net/france/paris,
                    https://en.wikipedia.org/wiki/List_of_diplomatic_missions_in_Paris,
                    https://www.paristopten.com/what-is-paris-syndrome/,
                    https://travelbetweenthepages.com/2024/01/08/paris-syndrome/,
                    https://www.myfrenchlife.org/2013/08/19/so-french-so-sick-the-paris-syndrome/,
                    https://www.tripzilla.com/the-paris-syndrome-why-asians-suffer-from-it/127572,
                    https://www.livescience.com/what-is-paris-syndrome,
                    https://wanderdolls.com/paris-syndrome-bs/,
                    https://en.wikipedia.org/wiki/Paris_syndrome,
                    https://writersblockmagazine.com/2021/11/23/paris-syndrome-romanticizing-your-life-and-changes/,
                    https://www.outlooktraveller.com/explore/inspiration/what-is-paris-syndrome,
                    https://www.sbs.com.au/news/article/paris-syndrome-culture-shock-sickness-sends-japanese-tourists-packing/t8a332he2,
                    https://www.independent.co.uk/travel/news-and-advice/what-is-paris-syndrome-b2477677.html,
                    https://www.islands.com/1579130/what-is-paris-syndrome/,
                    https://themaddifoundation.com/wp-content/uploads/2017/12/dailypost-2.pdf,
                    https://www.livescience.com/what-is-paris-syndrome"

            Given the URL, I want you to extract the following information from the webpages:

            * A list of mental health resources available at the {destination}, including:
                + Names of organizations, institutions, and agencies
                + Descriptions of the services offered
                + Contact information for each resource, including phone numbers, email addresses, and physical addresses
            * A list of crisis resources, including:
                + Hotlines and helplines
                + Online chat services
                + Emergency services and emergency contacts
                + Local resources and locations
            * Any relevant services, programs, or initiatives that support mental health, including:
                + Online resources and educational materials
                + Support groups and peer-to-peer services
                + Crisis intervention and emergency response services
            * Relevant information about the symptoms, causes, effects and other useful information related to Paris syndrome
            * List of embassies and diplomatic missions based on the user {origin}"""),
            expected_output = dedent(f"""
                    A list of the essential services like helplines, emergency contacts, embassies, diplomatic missions for the user to contact for help"""),
            agent=agent,
            output_file='resources.md'
            
        )

    def support_task(self, agent, origin, destination, answers, context):
        return Task(
            description=dedent(f"""
                I will provide you with an individual looking for guidance and advice on managing their emotions, stress, anxiety and other mental health issues arising due to Paris syndrome. 
                Use your knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other therapeutic methods in order to create strategies that the individual can implement in order to improve their overall wellbeing.
                Use the {answers} to provide the best advice. 
                {self.__tip_section()}

                Origin: {origin}
                Destination: {destination}
                Answers: {answers}
                """),
            expected_output=dedent("""
                The advice in markdown format highlighting:
                1. Key concerns expressed by the user.
                2. Emotional reassurance provided.
                3. Recommended coping strategies.
                4. Also, recommend any mental helplines in the {destination} if you have the correct information. Otherwise, do not provide any fake numbers.
                """),
            agent=agent,
            async_execution = False,
            context=[context],
            output_file = 'task1.md'
        )

    def cultural_task(self, agent, origin, destination, interests, context):
        return Task(
            description=dedent(f"""
                Educate the user about cultural differences and customs in {destination}.
                Provide tips on local etiquette and practices to help them adjust their expectations and also help address their problems.
                {self.__tip_section()}

                Origin: {origin}
                Destination: {destination}
                Interests: {interests}
                
                """),
            expected_output=dedent("""
                A cultural guide in markdown format that includes:
                1. Key cultural differences to be aware of.
                2. Local etiquette and customs.
                3. Tips for blending in and avoiding cultural misunderstandings.
                4. Recommendations for culturally immersive experiences based on the user's interests.
                """),
            async_execution = False,
            agent=agent,
            context=[context],
            output_file = 'task2.md'
            
        )

    def safety_advisor_task(self, agent, destination, context):
        return Task(
            description = dedent(f"""
                As an expert safety advisor, provide information on the following:
                * Suggest places to avoid, unsafe places along with reasoning
                * contact numbers of nearby police stations, hospitals, embassies and 
                * emergency services in the vicinity of the {destination}.
                * Safety tips and guidelines
                * Offer suggestions for safety procedures during traveling to avoid scams.{self.__tip_section()}
                """),
            expected_output = dedent(f"""
                Provide a comprehensive list of unsafe places, emergency services, safety tips and guidelines 
                and also the emergency contacts to reach out for help"""),
            agent = agent,
            context = [context],
            output_file = 'safety.md'
                
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100000!"