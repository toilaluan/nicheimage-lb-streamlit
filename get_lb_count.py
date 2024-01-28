import requests
import pandas as pd
from io import StringIO


def get_lb_count():
    fields = [
        "rewarding_realistic_vision",
        "rewarding_sdxl_turbo",
        "rewarding_anime_v3",
    ]
    # URL of the CSV file
    url = (
        "http://check_realistic_vision_nicheimage.nichetensor.com:15000/;csv;norefresh"
    )

    # Fetch the data
    response = requests.get(url)
    counter = {}

    # Check if the request was successful
    if response.status_code == 200:
        # Read the content of the response in a DataFrame
        csv_text = response.text
        data = pd.read_csv(StringIO(csv_text), sep=",")
        data = data[data.svname == "FRONTEND"].set_index("# pxname")
        total = 0
        for model in fields:
            counter[model] = int(data.loc[model, "stot"])
            total += counter[model]
        return counter
    else:
        print("Failed to retrieve data")

    # Now 'data' is a DataFrame containing your CSV data


if __name__ == "__main__":
    get_lb_count()
