from crewai import Crew
from agents import TravelAgents
from tasks import TravelTasks

from dotenv import load_dotenv


def main():
  load_dotenv()

  print("## Welcome to Trip Planner Crew")
  print('-------------------------------')
  days = input("For how many days will you be traveling?")
  
  interests = input("What are some of your interests and hobbies?")

  agents = TravelAgents()
  tasks = TravelTasks()

  local_guide = agents.local_guide()
  hotel_guide = agents.hotel_guide()
  travel_planner = agents.travel_planner()


  recommend_task = tasks.recommend(
        local_guide,
        interests,
        days
    )
  find_hotel_task = tasks.find_hotel(
        hotel_guide
    )
  plan_task = tasks.plan(
        travel_planner,
        interests,
        days
    )

  plan_task.context = [recommend_task, find_hotel_task]

  crew = Crew(
      agents=[
        local_guide, hotel_guide, travel_planner
      ],
      tasks=[recommend_task, find_hotel_task, plan_task],
      verbose=2,
      max_rpm=29
    )

  result = crew.kickoff(inputs={"interests": interests, "days": days})

  print("\n\n########################")
  print("## Here is you Trip Plan")
  print("########################\n")
  print(result)

  
if __name__ == "__main__":

    main()