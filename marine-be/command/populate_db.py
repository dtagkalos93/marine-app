import csv
import os
import json

import requests

URL = "http://localhost:8002/vessel-position/"


def populate_data():
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, 'data-fs-exercise.csv')
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            payload = json.dumps({
                "vessel_id": int(row["vessel_id"]),
                "position_time": row["position_time"],
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"])
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", URL, headers=headers, data=payload)
            if response.status_code != 201:
                print(payload)


if __name__ == "__main__":
    populate_data()
