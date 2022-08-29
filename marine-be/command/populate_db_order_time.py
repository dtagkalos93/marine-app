import os
import json

import requests
import pandas as pd

URL = "http://localhost:8002/vessel-position/"


def populate_data():
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, 'data-fs-exercise.csv')
    vessel_position_df = pd.read_csv(filename)
    vessel_position_df_sorted = vessel_position_df.sort_values(by=['position_time'],
                                                               ascending=True)

    for index, vessel_position in vessel_position_df_sorted.iterrows():
        payload = json.dumps({
            "vessel_id": int(vessel_position["vessel_id"]),
            "position_time": vessel_position["position_time"],
            "latitude": float(vessel_position["latitude"]),
            "longitude": float(vessel_position["longitude"])
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", URL, headers=headers, data=payload)
        if response.status_code != 201:
            print(payload)


if __name__ == "__main__":
    populate_data()
