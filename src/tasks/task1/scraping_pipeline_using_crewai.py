from crewai_tools import ScrapeWebsiteTool
import json
import pandas as pd

class DataPipeline:
    def __init__(self, website_url, output_filename):
        self.website_url = website_url
        self.output_filename = output_filename

    def fetch_data(self):
        # Initialize the scraping tool
        tool = ScrapeWebsiteTool(website_url=self.website_url)

        # Fetch JSON data
        json_text = tool.run()

        return json_text

    def process_data(self, json_text):
        if json_text:
            # Load JSON data
            data = json.loads(json_text)
            results = data.get('results', [])
            return results
        else:
            return []

    def save_data_to_csv(self, data):
        # Convert data to DataFrame
        final_df = pd.DataFrame(data)

        # Save DataFrame to CSV file
        final_df.to_csv(self.output_filename, index=False)

    def run_pipeline(self):
        # Fetch data
        json_text = self.fetch_data()

        # Process data
        results = self.process_data(json_text)

        # Save data to CSV
        self.save_data_to_csv(results)

def main():
    # Define a list of website URLs and corresponding output filenames
    websites_and_filenames = [
            ('https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-emplacement-des-stations/records?limit=-1&lang=en', 'metropole_stations.csv'),
            ('https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/paris-autrement-balades-dans-les-arrondissements-peripheriques-poi/records?limit=-1&lang=en', 'hidden_treasures.csv'),
            ]

    # Loop through the list and run the data ingestion pipeline for each website
    for website_url, output_filename in websites_and_filenames:
        # Create an instance of the DataPipeline class
        pipeline = DataPipeline(website_url, output_filename)

        # Run the data ingestion pipeline
        pipeline.run_pipeline()

if __name__ == "__main__":
    main()
