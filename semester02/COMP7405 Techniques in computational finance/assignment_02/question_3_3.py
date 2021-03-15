import csv
import numpy as np
from datetime import datetime
from question_1 import black_scholes_call, black_scholes_put


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

r = 0.04  # 4%
q = 0.2  # 20%

# (3.3)
# The trading unit for buying/selling an option is 10000, and the transaction
# cost is about 3.3 RMBs per unit. Using the non-arbitrage conditions you
# have learned so far, check whether you see any arbitrage opportunities in
# the data. You can consider two cases: one without any transaction cost, and
# the other one with the real transaction cost. You can assume there is no
# transaction cost for A50ETF. Write down your findings and submit them.


def call_put_parity(S, K, t, T, r, q):
    # C(S,t) - P(S,t) = Se^(-q(T - t)) - Ke^(-r(T - t))
    time = T - t
    return (S * np.exp(-q * (time))) - (K * np.exp(-r * (time)))


def write_result_to_text_file(text, file_name):
    # Open a file with access mode 'a'
    with open(file_name, "a") as file_object:
        # Append 'hello' at the end of file
        file_object.write(text)
        file_object.write("\n")

# Calculate call-put parity from 31.csv ()


def portfolio_estimation():
    filtered_data = []
    temp_object = {}

    for market in market_data:
        instrument = next(
            filter(lambda v: v['Symbol'] == market['Symbol'], instruments_data), None)

        if instrument['Symbol'] == '510050':
            temp_object['Last'] = market['Last']
            temp_object['Bid1'] = market['Bid1']
            temp_object['BidQty1'] = market['BidQty1']
            temp_object['Ask1'] = market['Ask1']
            temp_object['AskQty1'] = market['AskQty1']
            temp_object['LocalTime'] = market['LocalTime']
            filtered_data.append(temp_object)
            temp_object = {}
            continue

        if instrument['OptionType'] == 'C':
            temp_object['callLast'] = market['Last']
            temp_object['callBid'] = market['Bid1']
            temp_object['callBidQty'] = market['BidQty1']
            temp_object['callAsk'] = market['Ask1']
            temp_object['callAskQty'] = market['AskQty1']
            temp_object['callStrike'] = instrument['Strike']

        if instrument['OptionType'] == 'P':
            temp_object['putLast'] = market['Last']
            temp_object['putBid'] = market['Bid1']
            temp_object['putBidQty'] = market['BidQty1']
            temp_object['putAsk'] = market['Ask1']
            temp_object['putAskQty'] = market['AskQty1']
            temp_object['putStrike'] = instrument['Strike']

    with open("question_3_3_generated_data_table.csv", "w") as f:
        wr = csv.DictWriter(
            f, delimiter=",", fieldnames=list(filtered_data[0].keys()))
        wr.writeheader()
        wr.writerows(filtered_data)

    # Time to maturity
    T = (24 - 16) / 365

    sigma = 0.2

    # Clean up portfolio compare result file
    portfolio_compare_result_file = 'question_3_3_portfolio_compare.txt'
    open(portfolio_compare_result_file, 'w').close()

    for data in filtered_data:
        # Call - Put parity formula
        # C(S,t) - P(S,t) = Se^(-q(T - t)) - Ke^(-r(T - t))
        #
        # Portfolio A = C(S,t) + Ke^(-r(T - t))
        port_a = black_scholes_call(
            data['Last'], data['callStrike'], 0, T, r, sigma) + (data['callStrike'] * np.exp(-r * T))

        # Portfolio B = P(S,t) + Se^(-q(T - t))
        port_b = black_scholes_put(
            data['Last'], data['putStrike'], 0, T, r, sigma) + (data['Last'] * np.exp(-q * T))

        write_result_to_text_file('Equity 510050 at: {}'.format(
            data['LocalTime']), portfolio_compare_result_file)

        write_result_to_text_file(
            'Without Transaction cost', portfolio_compare_result_file)
        write_result_to_text_file('Portfolio A: {}'.format(
            port_a), portfolio_compare_result_file)
        write_result_to_text_file('Portfolio B: {}'.format(
            port_b), portfolio_compare_result_file)
        if port_a == port_b:
            write_result_to_text_file(
                'Portfolio A == Portfolio B: No Arbitrage oppotunity', portfolio_compare_result_file)
            write_result_to_text_file(
                '---------------------------------------------------', portfolio_compare_result_file)
            continue

        if port_a > port_b:
            write_result_to_text_file(
                'Portfolio A > Portfolio B: So we should Buy Portfolio A and Sell Portfolio B', portfolio_compare_result_file)

        if port_a < port_b:
            write_result_to_text_file(
                'Portfolio A < Portfolio B: So we should Buy Portfolio B and Sell Portfolio A', portfolio_compare_result_file)

        write_result_to_text_file(
            '--------------------------------------------------', portfolio_compare_result_file)

    return None


portfolio_estimation()
