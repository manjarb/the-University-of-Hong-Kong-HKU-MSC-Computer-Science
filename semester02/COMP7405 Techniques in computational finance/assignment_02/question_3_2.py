import csv
import numpy as np
from datetime import datetime
from question_3_1 import calculate_implied_volatility

market_data = []
instruments_data = []


def convert_local_time(date_time_string):
    return datetime.strptime(
        date_time_string, '%Y-%b-%d %H:%M:%S.%f').time().strftime("%H:%M:%S")


def create_date(date_time_string):
    return datetime.strptime(
        date_time_string, '%Y-%b-%d %H:%M:%S.%f')


with open('./marketdata.csv') as csv_file:
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        local_time = convert_local_time(row['LocalTime'])
        if local_time == '09:30:00' or local_time == '09:31:00' or local_time == '09:32:00' or row['Symbol'] == '510050':
            d_row = {}
            for key, value in row.items():
                if (key != 'LocalTime' and key != 'Symbol'):
                    d_row[key] = float(value)
                else:
                    d_row[key] = value

            market_data.append(d_row)


with open('./instruments.csv') as csv_file:
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        d_row = {}
        for key, value in row.items():
            if (key != 'Type' and key != 'OptionType' and key != 'Symbol' and value != ''):
                d_row[key] = float(value)
            else:
                d_row[key] = value

        instruments_data.append(d_row)


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
    options_31 = []
    options_32 = []
    options_33 = []
    q = 0.2  # 20%
    r = 0.04  # 4%
    # Time to maturity
    T = (24 - 16) / 365

    # Sample {'LocalTime': '2016-Feb-16 09:32:00.907981', 'Symbol': 10000566.0, 'Last': 0.0027, 'Bid1': 0.0026, 'BidQty1': 1.0, 'Ask1': 0.0035, 'AskQty1': 6.0}
    for index, market in enumerate(market_data):
        # Sample {'Type': 'Option', 'Symbol': 10000566.0, 'Expiry': 20160224.0, 'Strike': 1.8, 'OptionType': 'P'}
        option = next(
            filter(lambda v: v['Symbol'] == market['Symbol'], instruments_data), None)

        equity_symbol = next(
            filter(lambda v: v['Type'] == 'Equity', instruments_data), None)

        local_time = convert_local_time(market['LocalTime'])

        equity_price = 0
        for index_eq, market_eq in enumerate(market_data):
            if index_eq > index and market_eq['Symbol'] == equity_symbol['Symbol']:
                equity_price = market_eq['Last']
                break

        if option['Type'] != 'Option':
            continue

        K = option['Strike']
        bid_implied_volatility = calculate_implied_volatility(
            equity_price, K, 0, T, r, q, option['OptionType'], market['Bid1'])
        ask_implied_volatility = calculate_implied_volatility(
            equity_price, K, 0, T, r, q, option['OptionType'], market['Ask1'])

        bid_implied_volatility = 'NaN' if np.isnan(
            bid_implied_volatility) else bid_implied_volatility
        ask_implied_volatility = 'NaN' if np.isnan(
            ask_implied_volatility) else ask_implied_volatility

        if option['OptionType'] == 'P':
            # Calculate Bid Volatility
            data = {
                'Strike': K,
                'BidVolP': bid_implied_volatility,
                'AskVolP': ask_implied_volatility,
                'BidVolC': '',
                'AskVolC': '',
                'LocalTime': market['LocalTime'],
            }
        if option['OptionType'] == 'C':
            # Calculate Bid Volatility
            data = {
                'Strike': K,
                'BidVolP': '',
                'AskVolP': '',
                'BidVolC': bid_implied_volatility,
                'AskVolC': ask_implied_volatility,
                'LocalTime': market['LocalTime'],
            }

        if local_time == '09:30:00':
            options_31.append(data)

        if local_time == '09:31:00':
            options_32.append(data)

        if local_time == '09:32:00':
            options_33.append(data)

    if len(options_31) > 0:
        with open("31.csv", "w") as f:
            wr = csv.DictWriter(
                f, delimiter=",", fieldnames=list(options_31[0].keys()))
            wr.writeheader()
            wr.writerows(options_31)

    if len(options_32) > 0:
        with open("32.csv", "w") as f:
            wr = csv.DictWriter(
                f, delimiter=",", fieldnames=list(options_32[0].keys()))
            wr.writeheader()
            wr.writerows(options_32)

    if len(options_33) > 0:
        with open("33.csv", "w") as f:
            wr = csv.DictWriter(
                f, delimiter=",", fieldnames=list(options_33[0].keys()))
            wr.writeheader()
            wr.writerows(options_33)

    return None


calculate_bid_ask_implied_volatilities_all_instruments()
