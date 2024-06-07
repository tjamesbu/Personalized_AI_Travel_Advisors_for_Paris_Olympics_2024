import requests
import os
from dotenv import load_dotenv
import pandas as pd

class BicycleStationRealTimeInfo():
    def __init__(self) -> None:
        load_dotenv()
        self.out_folder_path = os.getenv('TRANSPORT_API_DATA_FOLDER_PATH')
        self.output_file = self.out_folder_path + "paris_bicycle_info_real_time.csv"
        self.station_info_url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"
        self.station_status_url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"

    def getInfo(self):
        '''
        Retrieve Paris bicycle station information and real-time status at each station from real-time API
        Source: Station Info @ https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json
                Station status @ https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json
            Parameters:
                    None
            Returns:
                    status (bool): response status
                    stationInfo_statusCode (int): response status code for stations' info
                    stationStatus_statusCode (int): response status code for stations' status
                    bicycleInfoFileName (str): absolute file path of paris_bicycle_info.csv
        '''
        
        station_info_response = requests.get(self.station_info_url)
        station_status_response = requests.get(self.station_status_url)

        if (station_info_response.status_code == 200) and (station_status_response.status_code == 200):
            status = True
            station_info = station_info_response.json()["data"]["stations"]
            station_status = station_status_response.json()["data"]["stations"]

            df_station_info = pd.DataFrame(station_info)
            df_station_status = pd.json_normalize(station_status)
            df = pd.merge(df_station_info, df_station_status, how="inner", on=["station_id", "stationCode"])
            df["rental_methods"] = df["rental_methods"].map(lambda x: "".join(x) if type(x)==list else "")
            df["mechanical_bikes"] = df["num_bikes_available_types"].map(lambda x: x[0]["mechanical"])
            df["ebike"] = df["num_bikes_available_types"].map(lambda x: x[1]["ebike"])

            df.to_csv(self.output_file, mode="w", index=False,
                      columns=["station_id","stationCode","name","lat","lon","capacity","rental_methods","num_bikes_available",
                               "numBikesAvailable","mechanical_bikes","ebike","num_docks_available",
                               "numDocksAvailable","is_installed","is_returning","is_renting","last_reported"])
        else:
            status = False

        return status, station_info_response.status_code, station_status_response.status_code, self.output_file
