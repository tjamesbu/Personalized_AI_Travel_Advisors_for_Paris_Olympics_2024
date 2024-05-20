prompt_template = '''
You are the Garder, an AI travel assistant focused on raising safety awareness for travelers visiting Paris. 
Your goal is to provide comprehensive information on areas to avoid, nearby police stations, and embassies, as well as 
general safety procedures to enhance their trip.

Hello adventurer! Want to learn about safety procedures for your trips in Paris?

What is your current location in Paris?
- Suggestions: "I'm at the Eiffel Tower.", "I'm in Montmartre."

Where are you from? (for nearby embassy)
- Suggestions: "I'm from the USA.", "I'm from Germany."

Based on your responses, I'll provide relevant safety information.

1. Suggest places to avoid in Paris.

2. Provide information about nearby police stations.

3. Provide information about nearby embassies.

4. Offer suggestions for safety procedures during traveling to avoid scams.

5. End the conversation with: "Stay safe and have a nice trip!"
'''

import requests

def get_police_stations(location):
   """Placeholder function to retrieve nearby police stations based on location"""
   if location.lower() == "eiffel tower":
       return "36 Quai des Orfèvres"
   elif location.lower() == "montmartre":
       return "12 Rue Cauchois"
   else:
       return "Please specify a more common tourist location for precise police station information."

def get_embassies(country):
   """Placeholder function to retrieve nearby embassies based on country"""
   if country.lower() == "usa":
       return "2 Avenue Gabriel, 75008 Paris"
   elif country.lower() == "germany":
       return "13/15 Avenue Franklin D. Roosevelt, 75008 Paris"
   else:
       return "Please specify a valid country for embassy information."

def generate_response(location, country):
   responses = []

   responses.append("1. Suggest places to avoid in Paris:")
   responses.append("- Avoid the areas around Gare du Nord and certain parts of the 18th arrondissement at night.")
   responses.append("- Exercise caution in crowded tourist areas like the Louvre and Notre-Dame Cathedral, especially during peak hours.")
   responses.append("- Be vigilant in public transportation, particularly on metro lines with high tourist traffic.")

   responses.append("\n2. Information about nearby police stations:")
   police_station = get_police_stations(location)
   responses.append(f"The nearest police station to your location is at {police_station}.")

   responses.append("\n3. Information about nearby embassies:")
   embassy_address = get_embassies(country)
   responses.append(f"The nearest embassy based on your country of origin is located at {embassy_address}.")

   responses.append("\n4. Suggestions for safety procedures during traveling to avoid scams:")
   responses.append("- Be cautious of pickpockets and scam artists, especially in crowded areas and tourist attractions.")
   responses.append("- Keep your belongings secure and avoid displaying expensive items in public.")

   responses.append("\n5. Stay safe and have a nice trip!")

   return '\n'.join(responses)

# Example usage:
location = "Eiffel Tower"
country = "USA"
print(generate_response(location, country))