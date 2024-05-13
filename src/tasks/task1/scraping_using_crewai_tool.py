from crewai_tools import ScrapeWebsiteTool
import json
import pandas as pd

# Define the website URL
website_url = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/que-faire-a-paris-/records?limit=-1'

all_results = []

# Initialize the scraping tool
tool = ScrapeWebsiteTool(website_url=website_url)

# Fetch JSON data for the current batch
json_text = tool.run()

# Check if JSON text is not empty
if json_text:
    # Load JSON data
    data = json.loads(json_text)
    results = data.get('results', [])
    
    # Check if results exist
    if results:
        # Append current batch of results to the list
        all_results.extend(results)
            
# Convert all results to a DataFrame
final_df = pd.DataFrame(all_results)

# Save DataFrame to CSV file
final_df.to_csv("events.csv", index=False)

