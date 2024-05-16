prompt_template_name = PromptTemplate(
        input_variables=["range", "origin", "destination", "interests"],
        template=("""As a local expert on this city you must compile an 
        in-depth guide for someone traveling there and wanting 
        to have THE BEST trip ever!
        Gather information about the following:
        1. Uncover unique festivals, hidden gems/treasures and hidden restaurants frequented by locals, quirky shops, and off-the-beaten-path experiences (e.g., attending a local sports event, visiting a community art space, exploring lesser-known historical sites).
        2. Describe the sights, sounds, and smells that bring the city to life (e.g., the bustling energy of a morning market, the breathtaking views from a specific viewpoint, the aroma of freshly baked bread from a local bakery).
        3 .Go beyond basic customs. Include interesting traditions, etiquette specific to certain situations, or local expressions visitors might encounter.
        4. Highlight local delicacies beyond the typical tourist fare (e.g., street food stalls with unique dishes, hidden restaurants serving regional specialties, cooking classes to learn local cuisine).
        5. Mention how weather impacts the experience (e.g., winter festivals, outdoor activities best suited for specific seasons).
        6. Briefly mention how costs might fluctuate depending on the season and travel style (e.g., peak season flight prices, budget-friendly transportation options).
        7. Suggest eco-friendly activities (e.g., using public transport, visiting sustainable businesses).
        8. Include information on accessibility options for landmarks and activities.
        9. Provide recommendations for experiencing the city's nightlife scene based on the target audience (e.g., live music venues, local bars, cultural performances).
        
        The final answer must be a comprehensive city guide, 
        rich in cultural insights and practical tips, 
        tailored to enhance the travel experience.
        Trip Date: {range}
        Traveling from: {origin}
        Traveling to: {destination}
        Traveler Interests: {interests}
        """)
    )