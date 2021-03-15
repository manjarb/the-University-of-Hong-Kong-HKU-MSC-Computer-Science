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


with open('./instruments.csv') as csv_file:
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        d_row = {}
        for key, value in row.items():
            if (key != 'Type' and key != 'OptionType' and key != 'Symbol' and value != ''):
                d_row[key] = float(value)
            else:
                d_row[key] = value

        instruments_data.append(d_row)


with open('./marketdata.csv') as csv_file:
    for row in csv.DictReader(csv_file, skipinitialspace=True):
        local_time = convert_local_time(row['LocalTime'])
        d_row = {}
        for key, value in row.items():
            if (key != 'LocalTime' and key != 'Symbol'):
                d_row[key] = float(value)
            else:
                d_row[key] = value

        market_data.append(d_row)


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

def compute_latest_data(data_list, exit_key, exit_value, spot_key, spot_value):
    result = []
    for index, data in enumerate(data_list):
        exit_time = convert_local_time(data[exit_key])
        result_index = next((index for (index, d) in enumerate(
            result) if d["Symbol"] == data['Symbol']), None)

        if result_index is None:
            result.append(data)
        else:
            result.pop(result_index)
            result.append(data)

        if exit_time == exit_value:
            break

    last_spot_index = 0
    for index, value in enumerate(result):
        if value[spot_key] == spot_value:
            last_spot_index = index

    result = result[:(last_spot_index + 1)]

    return result


def compute_implied_volatility(data, instruments, T, r, q):
    # Sample {'LocalTime': '2016-Feb-16 09:32:00.907981', 'Symbol': 10000566.0, 'Last': 0.0027, 'Bid1': 0.0026, 'BidQty1': 1.0, 'Ask1': 0.0035, 'AskQty1': 6.0}
    implied_volatility = []
    equity_price = data[-1]
    for index, market in enumerate(data):
        instrument = next(
            filter(lambda v: v['Symbol'] == market['Symbol'], instruments), None)

        if instrument['Type'] != 'Option':
            continue

        computed_data = {}
        K = instrument['Strike']

        bid_implied_volatility = calculate_implied_volatility(
            equity_price['Last'], K, 0, T, r, q, instrument['OptionType'], market['Bid1'])
        ask_implied_volatility = calculate_implied_volatility(
            equity_price['Last'], K, 0, T, r, q, instrument['OptionType'], market['Ask1'])

        bid_implied_volatility = 'NaN' if np.isnan(
            bid_implied_volatility) else bid_implied_volatility
        ask_implied_volatility = 'NaN' if np.isnan(
            ask_implied_volatility) else ask_implied_volatility

        if instrument['OptionType'] == 'P':
            # Calculate Implied Volatility
            computed_data = {
                'Strike': K,
                'BidVolP': bid_implied_volatility,
                'AskVolP': ask_implied_volatility,
                'BidVolC': '',
                'AskVolC': '',
                'Symbol': market['Symbol'],
                'LocalTime': market['LocalTime'],
            }
        if instrument['OptionType'] == 'C':
            # Calculate Implied Volatility
            computed_data = {
                'Strike': K,
                'BidVolP': '',
                'AskVolP': '',
                'BidVolC': bid_implied_volatility,
                'AskVolC': ask_implied_volatility,
                'Symbol': market['Symbol'],
                'LocalTime': market['LocalTime'],
            }

        implied_volatility.append(computed_data)

    return implied_volatility


def create_result_file(result_file_name, iv_data):
    with open(result_file_name, "w") as f:
        wr = csv.DictWriter(
            f, delimiter=",", fieldnames=list(iv_data[0].keys()))
        wr.writeheader()
        wr.writerows(iv_data)


def calculate_bid_ask_implied_volatilities_all_instruments():
    # Compute 09:31:00 Data
    options_31 = compute_latest_data(
        market_data, 'LocalTime', '09:31:00', 'Symbol', '510050')

    # Compute 09:32:00 Data
    options_32 = compute_latest_data(
        market_data, 'LocalTime', '09:32:00', 'Symbol', '510050')

    # Compute 09:33:00 Data
    options_33 = compute_latest_data(
        market_data, 'LocalTime', '09:33:00', 'Symbol', '510050')
    q = 0.2  # 20%
    r = 0.04  # 4%
    # Time to maturity
    T = (24 - 16) / 365

    iv_31 = compute_implied_volatility(options_31, instruments_data, T, r, q)
    iv_32 = compute_implied_volatility(options_32, instruments_data, T, r, q)
    iv_33 = compute_implied_volatility(options_33, instruments_data, T, r, q)

    # Create implied volatility result
    create_result_file("31.csv", iv_31)
    create_result_file("32.csv", iv_32)
    create_result_file("33.csv", iv_33)

    return None


calculate_bid_ask_implied_volatilities_all_instruments()
