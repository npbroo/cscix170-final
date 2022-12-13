""" Utility code."""

import os
import pandas as pd
import matplotlib.pyplot as plt
DATA_DIR = "data"
def symbol_to_path(symbol, base_dir=os.path.join("", DATA_DIR)):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def plot_data(df_main, dfs=[], order_book=[], title="Portfolio Value", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df_main.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    for df in dfs:
        df.plot(ax=ax)

    for order in order_book:
        if(order['Order'] == 'BUY'):
            plt.axvline(x=order['Date'], color='green')
        elif(order['Order'] == 'SELL'):
            plt.axvline(x=order['Date'], color='red')

    plt.show()

def get_data(symbols, dates, addSPY=True, colname = 'Adj Close', dir=DATA_DIR):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol, dir), index_col='Date',
                parse_dates=True, usecols=['Date', colname], na_values=['nan'])
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df