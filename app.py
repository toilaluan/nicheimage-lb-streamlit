from get_lb_count import get_lb_count
import streamlit as st
import time
import matplotlib.pyplot as plt
import datetime
import json
from threading import Thread
import pandas as pd


total_data = {}


# create a thread to get data each hour
def get_data():
    global total_data
    i = 0
    while True:
        today_data = total_data.setdefault(str(datetime.date.today()), {})
        hour = datetime.datetime.now().hour
        data = get_lb_count()
        today_data[hour] = data
        i += 1
        with open("data.json", "w") as f:
            json.dump(total_data, f)
        time.sleep(3600)


# Data for the plot
if __name__ == "__main__":
    # thread = Thread(target=get_data)
    # thread.start()

    data = json.load(open("data.json", "r"))
    print(data)
    colors = ["#ff9999", "#66b3ff", "#99ff99"]

    # plot ECharts by day
    st.title("Nichetensor LB Distribution")

    records = []
    for date, hours in data.items():
        for hour, categories in hours.items():
            for category, value in categories.items():
                records.append(
                    {"date": date, "hour": hour, "category": category, "value": value}
                )

    df = pd.DataFrame(records)

    # Plot the pie chart for the most recent hour
    latest_data = df[df["hour"] == df["hour"].max()].groupby("category")["value"].sum()
    try:
        previous_data = (
            df[df["hour"] == str(int(df["hour"].max()) - 1)]
            .groupby("category")["value"]
            .sum()
        )
    except Exception as e:
        print(e)
        previous_data = None
    # substract the previous data from the latest data
    if previous_data is not None:
        latest_data = latest_data - previous_data
    else:
        latest_data = latest_data
    print(latest_data)
    fig2, ax2 = plt.subplots()
    ax2.pie(latest_data, labels=latest_data.index, autopct="%1.1f%%")
    ax2.set_title("Distribution in Recent Hour")

    # Display the plots in Streamlit
    st.pyplot(fig2)
