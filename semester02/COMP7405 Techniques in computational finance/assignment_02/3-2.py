import csv
import numpy as np
from datetime import datetime

market_data = []
instruments_data = []

with open('./marketdata.csv') as csv_file:
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        local_time = datetime.strptime(
            row['LocalTime'], '%Y-%b-%d %H:%M:%S.%f').time().strftime("%H:%M:%S")
        if local_time == '09:31:00' or local_time == '09:32:00' or local_time == '09:33:00':
            d_row = {}
            for key, value in row.items():
                if (key != 'LocalTime'):
                    d_row[key] = float(value)
                else:
                    d_row[key] = value

            market_data.append(d_row)


with open('./instruments.csv') as csv_file:
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        d_row = {}
        for key, value in row.items():
            if (key != 'Type' and key != 'OptionType' and value != ''):
                d_row[key] = float(value)
            else:
                d_row[key] = value

        instruments_data.append(d_row)


print(np.array(market_data))
print(np.array(instruments_data))

# (3.2)
# Apply your algorithm to calculate the implied volatilities
# for both the bid prices and the ask prices. Specically, you need:

# (3.2.1)
# calculate the bid/ask implied volatilities of all instruments at
# 09:31:00, 09:32:00, 09:33:00.
# Specifically, you take snapshots of the given market data at
# 09:31:00, 09:32:00, 09:33:00, respectively.
# Then for each snapshot,
# you calculate the bid implied volatility and ask implied volatility of each instrument.
# Put your results in three separate csv files
# using the names "31.csv", "32.csv", and "33.csv"
# (this is to make our tutor's life easier, thank you).
# The csv les should have the following format:
# ----------------------------------------------
# Strike | BidVolP | AskVolP | BidVolC | AskVolC
#   1.9  |  ....   |  ....   |  ....   |  ....


def calculate_bid_ask_implied_volatilities_all_instruments():

    return None
