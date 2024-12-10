# video script here
# explain imports
# set up user input for stock
# setting up api key
# establishing list for times and prices, store the data

import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
from datetime import datetime, timedelta
import time

# setting up api key
# remember to set stock symbol to a user input
# create a user input that allows you to choose date 
# User inputs for stock symbol and date
user_input = input("Which stock? Please enter the ticker: ").upper()
unmodified_date = input("On which day do you want to track this stock? Enter in YYYY-MM-DD format: ")

# have to minus one day back for timeframe to capture one whole day on the plot
# have to convert date to strings
stripped_date = datetime.strptime(unmodified_date, "%Y-%m-%d")
modified_date = stripped_date - timedelta(days=1)
start_date = modified_date.strftime("%Y-%m-%d")
end_date = stripped_date.strftime("%Y-%m-%d")

#setting up the API key and create user input variable to store what they want tracked
# edit link so that it can align with what the user wants
API_KEY = "Tihe5QdbsnVOt78mMHkrvnm6Fxup4tMi"
STOCK_SYMBOL = user_input
url = f"https://api.polygon.io/v2/aggs/ticker/{STOCK_SYMBOL}/range/5/minute/{start_date}/{end_date}?apiKey={API_KEY}"

times = []
prices = []

# setting up plot using matplotlib
# create grid using subplots 
# text is way too big, rotate to fit it in 
# x.label and y.label to set the text on the sides
fig, ax = plt.subplots()
line, = ax.plot_date(times, prices, '-')
plt.title(f"{STOCK_SYMBOL} Brandon Tran Stock Tracker 2024, in 1 minute intervals")
plt.xlabel("Time")
plt.ylabel("Price in USD")
plt.xticks(rotation=30)
plt.grid(True)

# creating function for grabbing data 
def grab_api_data():
    try:
        response = requests.get(url)
        data = response.json()
        if 'results' not in data:
            print("Unexpected response structure:", data)
            return None

        timestamps = [datetime.utcfromtimestamp(item['t'] / 1000) for item in data['results']]

        close_prices = [item['c'] for item in data['results']]  

        return timestamps, close_prices
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Function to update the graph with the latest data
def update(frame):
    data = grab_api_data()
    
    if data:
        timestamps, close_prices = data

        # have to append (put at the last) 100 data points from graph.
        # use -100: for the whole day
        #IMPORTANT USE -100 FOR WHOLE DAY!!!
        times.extend(timestamps)
        prices.extend(close_prices)
        times_to_plot = times[-100:]
        prices_to_plot = prices[-100:]

        # setting up plot data
        # auto resize window
        line.set_data(times_to_plot, prices_to_plot)
        ax.relim()
        ax.autoscale_view()

    return line,

# repeat animation to update every 12 seconds (5 requests per minute API limitation)
ani = animation.FuncAnimation(fig, update, interval=12000)
plt.tight_layout()
plt.show()
