import csv
import numpy as np
import pandas as pd
from datetime import datetime
from question_3_1 import calculate_implied_volatility

market_data = []
instruments_data = []

with open('./marketdata.csv') as csv_file:
    for row in csv.DictReader(csv_file, skipinitialspace=True):
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

q = 0.2  # 20%
r = 0.04  # 4%

# (3.3)
# The trading unit for buying/selling an option is 10000, and the transaction
# cost is about 3.3 RMBs per unit. Using the non-arbitrage conditions you
# have learned so far, check whether you see any arbitrage opportunities in
# the data. You can consider two cases: one without any transaction cost, and
# the other one with the real transaction cost. You can assume there is no
# transaction cost for A50ETF. Write down your ndings and submit them.


def call_put_parity(S, K, t, T, r, q):
    # C(S,t) - P(S,t) = Se^(-q(T - t)) - Ke^(-r(T - t))
    time = T - t
    return (S * np.exp(-q * (time))) - (K * np.exp(-r * (time)))

# Calculate call-put parity from 31.csv ()


def portfolio_estimation():
    filtered_data = []
    temp_object = {}

    for market in market_data:
        instrument = next(
            filter(lambda v: v['Symbol'] == market['Symbol'], instruments_data), None)

        if instrument['Symbol'] == '510050':
            temp_object['last'] = market['Last']
            temp_object['Bid1'] = market['Bid1']
            temp_object['BidQty1'] = market['BidQty1']
            temp_object['Ask1'] = market['Ask1']
            temp_object['AskQty1'] = market['AskQty1']
            filtered_data.append(temp_object)
            temp_object = {}
            continue

        if instrument['OptionType'] == 'C':
            temp_object['callLast'] = market['Last']
            temp_object['callBid'] = market['Bid1']
            temp_object['callBidQty'] = market['BidQty1']
            temp_object['callAsk'] = market['Ask1']
            temp_object['callAskQty'] = market['AskQty1']

        if instrument['OptionType'] == 'P':
            temp_object['putLast'] = market['Last']
            temp_object['putBid'] = market['Bid1']
            temp_object['putBidQty'] = market['BidQty1']
            temp_object['putAsk'] = market['Ask1']
            temp_object['putAskQty'] = market['AskQty1']

    # If new data need to print
    # df = pd.DataFrame(filtered_data)
    # print(df)

    for data in filtered_data:
      # Call - Put parity formula
      # C(S,t) - P(S,t) = Se^(-q(T - t)) - Ke^(-r(T - t))
      # 
      # Portfolio A = C(S,t) + Ke^(-r(T - t))

      # Portfolio B = P(S,t) + Se^(-q(T - t))

    return None


portfolio_estimation()
