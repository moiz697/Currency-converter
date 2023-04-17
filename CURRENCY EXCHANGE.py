import requests
import tkinter as tk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
# set up the GUI window
root = tk.Tk()
root.title("Currency Converter")

# define the functions


def convert_currency():
    # get the input values from the widgets
    amount = float(amount_entry.get())
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    API = "39a2db81b7c748d7bfa631556efbcf5c"
    # make a GET request to the Currency Data API with your API key
    url = f"https://openexchangerates.org/api/latest.json?app_id={API}"
    response = requests.get(url).json()
    print(response)

    # check if the 'rates' key is present in the response dictionary
    if 'rates' in response:
        # parse the response JSON to get the exchange rate
        rates = response["rates"]
        # check if the from and to currencies are present in the rates dictionary
        if from_currency in rates and to_currency in rates:
            # calculate the converted amount
            converted_amount = amount * (rates[to_currency]/rates[from_currency])
            # update the result label
            result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
        else:
            result_label.config(text="Error: invalid currency selection")
    else:
        result_label.config(text="Error: failed to retrieve exchange rates")

def create_graph(exchange_rates):
    # extract the currency symbols and rates from the exchange_rates dictionary
    currencies = list(exchange_rates.keys())
    rates = list(exchange_rates.values())

    # create a figure and axis object
    fig, ax = plt.subplots()

    # create a line graph with currency symbols on the x-axis and rates on the y-axis
    ax.plot(currencies, rates)

    # set the title and axis labels
    ax.set_title("Exchange Rates")
    ax.set_xlabel("Currency")
    ax.set_ylabel("Rate")

    # rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # display the graph
    plt.show()
def reset():
    amount_entry.delete(0, tk.END)
    result_label.config(text="")

def update_rates():
    response = requests.get("https://api.exchangeratesapi.io/latest")
    if response.status_code == 200:
        # parse the JSON response to get the exchange rates
        exchange_rates = response.json()["rates"]
        # update the currency rate label
        rate_label.config(text=f"Currency Rates (as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}): {exchange_rates}")
        # create and display the graph
        create_graph(exchange_rates)
    else:
        rate_label.config(text="Error: failed to retrieve exchange rates")
    # schedule the next update in 60 seconds
    root.after(60000, update_rates)


# create the widgets
currencies = ["USD", "EUR", "JPY", "GBP", "CAD", "AUD", "CHF", "CNY", "HKD", "NZD"]

from_currency_var = tk.StringVar(root)
from_currency_var.set(currencies[0])  # default value
from_currency_menu = tk.OptionMenu(root, from_currency_var, *currencies)
from_currency_menu.pack(side=tk.LEFT, padx=10)

to_currency_var = tk.StringVar(root)
to_currency_var.set(currencies[1])  # default value
to_currency_menu = tk.OptionMenu(root, to_currency_var, *currencies)
to_currency_menu.pack(side=tk.LEFT, padx=10)

amount_label = tk.Label(root, text="Amount:")
amount_label.pack(side=tk.LEFT, padx=10)

amount_entry = tk.Entry(root)
amount_entry.pack(side=tk.LEFT)

convert_button = tk.Button(root, text="Convert", command=convert_currency)
convert_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(root, text="Reset", command=reset)
reset_button= tk.Button(root, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT, padx=10)
result_label = tk.Label(root, text="")
result_label.pack(side=tk.LEFT, padx=10)
root.mainloop()