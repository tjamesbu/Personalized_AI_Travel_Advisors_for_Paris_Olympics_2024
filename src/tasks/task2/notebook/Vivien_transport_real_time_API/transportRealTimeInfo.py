import requests
import os
from dotenv import load_dotenv
import datetime
import pandas as pd
import datetime
from bs4 import BeautifulSoup

class TransportRealTimeInfo():
    def __init__(self) -> None:
        load_dotenv()
        self.prim_api_key = os.getenv('PARIS_PRIM_API_KEY')
        self.out_folder_path = os.getenv('TRANSPORT_API_DATA_FOLDER_PATH')
        self.output_file = self.out_folder_path + "paris_traffic_info_real_time.csv"
        self.headers = {'Accept':'application/json', 'apikey': self.prim_api_key}
        self.url = "https://prim.iledefrance-mobilites.fr/marketplace/disruptions_bulk/disruptions/v2"

    def remove_tags(self, html):
        # parse html content
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()
        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)

    def convertDate(self, datestring):
        return datetime.datetime.strptime(datestring, '%Y%m%dT%H%M%S')

    def getStartDate(self, dates):
        return self.convertDate(dates[0]["begin"])

    def getEndDate(self, dates):
        return self.convertDate(dates[0]["end"])
    
    def getInfo(self):
        '''
        Retrieve current and future traffic disruption messages in ile de France from real-time API
        Source: Info Trafic Global Query @ https://prim.iledefrance-mobilites.fr/en/apis/idfm-disruptions_bulk
            Parameters:
                    None
            Returns:
                    status (bool): response status
                    statusCode (int): response status code
                    trafficInfoFileName (str): absolute file path of paris_traffic_info.csv
        '''
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            status = True
            df = pd.json_normalize(response.json()["disruptions"])
            df["startDate"] = df["applicationPeriods"].map(self.getStartDate)
            df["endDate"] = df["applicationPeriods"].map(self.getEndDate)
            df["lastUpdate"] = df["lastUpdate"].map(self.convertDate)
            df["message_nohtml"] = df["message"].map(self.remove_tags)
            df["tags"] = df["tags"].map(lambda val: "".join(val) if type(val)==list else val)

            df.drop(["id","applicationPeriods"], axis=1, inplace=True)
            df.to_csv(self.output_file, mode="w", index=False,
                      columns=["startDate","endDate","lastUpdate","cause","severity","title","message","message_nohtml","tags"])
        else:
            status = False

        return status, response.status_code, self.output_file