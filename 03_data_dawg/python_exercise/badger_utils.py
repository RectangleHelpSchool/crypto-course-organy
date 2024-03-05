from web3 import Web3
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

NODE_PROVIDER = 'https://eth-mainnet.g.alchemy.com/v2/7s0nlb02rkkhdjj6su89JmyHVFgsm6kW'

# validated on 31/8/2021
START_BLOCK = 13135622

# validated on 1/1/2022
END_BLOCK = 13915631

w3 = Web3(Web3.HTTPProvider(NODE_PROVIDER))


def heuristic(start_block: int, end_block: int) -> int:
    events = w3.eth.get_logs({
        'fromBlock': start_block,
        'toBlock': end_block,
        'topics': [
            '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'
        ],
        'address': '0x4b92d19c11435614CD49Af1b589001b7c08cD4D5'
    })

    df = pd.DataFrame(events)

    if df.empty:
        return 0

    grouped_df = df.groupby(df['topics'].str[2]).size().reset_index(name='count')
    return max(grouped_df['count'])


def generate_graph(start_block, end_block, interval):
    x_values = []
    y_values = []

    current_block = start_block
    while current_block <= end_block:
        x_values.append(current_block)
        y_values.append(heuristic(current_block, current_block + interval))

        current_block += interval

    plt.plot(x_values, y_values)
    plt.xlabel('Block Numbers')
    plt.ylabel('Heuristic Result')
    plt.title(f'Heuristic Function Results ({start_block} to {end_block}, Interval: {interval})')
    plt.show()


generate_graph(START_BLOCK, END_BLOCK, 20000)
