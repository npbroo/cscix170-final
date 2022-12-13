""" HW4 : Market simulator."""

import pandas as pd
import numpy as np
from util import get_data, plot_data
from strategies.bbands_rsi_strategy import BBANDS_RSI_STRAT

def compute_portvals(order_book, start_val=1000000, commission=9.95, impact=0.005, verbose=False):
    # this is the function the autograder will call to test your code
    # TODO: Your code here

    # get the orders and sort them by date
    if(verbose):print(order_book)
    orders = pd.DataFrame(order_book)#pd.read_csv(orders_file, parse_dates=True, index_col='Date', na_values=['nan'], usecols=['Date', 'Symbol', 'Order', 'Shares'])
    orders = orders.set_index('Date')
    orders.sort_index(inplace=True)

    # find all distinct symbols in list
    symbols = np.array(orders.Symbol.unique()).tolist()

    # get all the prices
    start_date = orders.index[0]
    end_date = orders.index[-1]
    prices = get_data(symbols, pd.date_range(start_date, end_date))
    prices = prices.reindex(sorted(prices.columns), axis=1)

    # create a dictionary to track currently open shares
    open_orders = {}
    for s in symbols:
        open_orders[s] = 0
    open_orders['cash'] = start_val

    # create an empty dataframe to store the daily values for the timeframe
    daily_values = pd.DataFrame(prices.iloc[0:], columns=['Daily Value'])
    daily_values = daily_values.fillna(0)

    # calculate the daily values
    for date, price in prices.iterrows():
        for order_date, order in orders.iterrows():
            if date == order_date:
                if(order['Order']) == 'BUY':
                    open_orders[order['Symbol']] += order['Shares']
                    value = price[order['Symbol']] * order['Shares']
                    open_orders['cash'] -= value
                    open_orders['cash'] -= (value*impact + commission)
                elif(order['Order']) == 'SELL':
                    open_orders[order['Symbol']] -= order['Shares']
                    value = price[order['Symbol']] * order['Shares']
                    open_orders['cash'] += value
                    open_orders['cash'] -= (value*impact + commission)
        total = 0

        # sum all of the currently open shares * their prices 
        for symbol in open_orders:
            if symbol == 'cash':
                total += open_orders[symbol]
            else:
                total += price[symbol] * open_orders[symbol]
        daily_values.loc[date, 'Daily Value'] = total
    return daily_values

def get_portfolio_stats(port_val, samples_per_year=252, daily_rf=0):
    daily_ret = port_val.pct_change()
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    cum_ret = port_val / port_val.iloc[0] - 1
    cum_ret = cum_ret[-1]
    sharpe_ratio = np.sqrt(samples_per_year) * np.mean(daily_ret - daily_rf) / std_daily_ret
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio

def get_portfolio_value(prices, allocs, start_val):
    normed = prices / prices.iloc[0]
    allocated = normed * allocs
    pos_vals = allocated * start_val
    port_vals = pos_vals.sum(axis=1)
    return port_vals

def calculate_profit(ticker, start_date, end_date, sv, parameters):
    shares_per_trade = 1000
    ticker_prices = get_data([ticker], pd.date_range(start_date, end_date), addSPY=False).dropna()
    order_book = bollinger_rsi_strat(ticker_prices, ticker, shares_per_trade, parameters)
    portvals = compute_portvals(order_book=order_book, start_val=sv)
    return portvals[portvals.columns[0]][-1] # return the final portfolio value

def RunCode():
    # Define input parameters below

    sv = 100000
    start_date = '2000-02-10'
    end_date = '2012-06-10'
    ticker = 'SPY'
    # Strategy Parameters
    new_params = {
            # = updated
            'bollinger_window': 9,#      # the window to use when calculating the bollinger bands
            'rsi_window': 14,            # the window to use when calculating the rsi
            'rsi_buy_threshold': 42,#    # rsi must be above the rsi buy threshold in order to buy
            'max_positions': 3,#         # the max number of open positions
            'take_profit_%': 0.15,       # if an open order has a net gain of greater to or equal to the take profit percent then close the order
            'stop_loss_%': 0.03          # if an open order has a net loss greater to or equal to the stop loss then close the order
    }

    # get portfolio stats for teh ticker
    ticker_prices = get_data([ticker], pd.date_range(start_date, end_date), addSPY=False)
    ticker_prices = ticker_prices.dropna()

    # create new strategy object and set the parameters
    strategy = BBANDS_RSI_STRAT(verbose=True)
    strategy.set_params(new_params)
    order_book = strategy.run_strategy(ticker_prices, ticker, 1000)

    # Process orders
    portvals = compute_portvals(order_book=order_book, start_val=sv)

    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    prices_SPY = get_data(['SPY'], pd.date_range(start_date, end_date), addSPY=False)
    portvals_SPY = get_portfolio_value(prices_SPY, [1.0], start_val = sv)
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = get_portfolio_stats(portvals_SPY)

    # Compare portfolio against SPY
    print( f"Start Date:  \t\t\t{start_date}" )
    print( f"End Date:    \t\t\t{end_date}" )

    print("")
    print( f"Sharpe Ratio of Fund: \t\t{sharpe_ratio}")
    print( f"Sharpe Ratio of SPY:  \t\t{sharpe_ratio_SPY}\n")

    print( f"Cumulative Return of Fund: \t{cum_ret}")
    print( f"Cumulative Return of SPY : \t{cum_ret_SPY}\n")

    print( f"Standard Deviation of Fund: \t{std_daily_ret}")
    print( f"Standard Deviation of SPY : \t{std_daily_ret_SPY}\n")

    print( f"Average Daily Return of Fund: \t{avg_daily_ret}")
    print( f"Average Daily Return of SPY : \t{avg_daily_ret_SPY}\n")

    print( f"Final Portfolio Value: \t\t{portvals[-1]}")

    plot_data(portvals, [portvals_SPY], order_book=order_book)

if __name__ == "__main__":
    RunCode()