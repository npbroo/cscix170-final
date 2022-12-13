import sys
sys.path.append("..")
from util import plot_data
from .indicators.bollinger_bands import bollinger_bands_indicator
from .indicators.rsi import rsi_indicator
import numpy as np
from .abstract_strategy import Strategy

class BBANDS_RSI_STRAT(Strategy):

    params = {}

    def __init__(self, verbose=False):
        default_params = {
            'bollinger_window': 20,     # the window to use when calculating the bollinger bands
            'rsi_window': 14,           # the window to use when calculating the rsi
            'rsi_buy_threshold': 40,    # rsi must be above the rsi buy threshold in order to buy
            'max_positions': 1,         # the max number of open positions
            'take_profit_%': 0.15,      # if an open order has a net gain of greater to or equal to the take profit percent then close the order
            'stop_loss_%': 0.03         # if an open order has a net loss greater to or equal to the stop loss then close the order
        }
        super().__init__(default_params, verbose)
        self.set_params()

    def set_params(self, params={}):
        self.params = self.load_parameters(params)

    def run_strategy(self, portvals, name, shares_per_trade):

        # LOAD INDICATORS
        # loads indicators required for strategy
        portvals = bollinger_bands_indicator(portvals, name, window=self.params['bollinger_window']) # add bollinger bands info to portvals
        if(self.verbose): plot_data(portvals)
        portvals = rsi_indicator(portvals, name, window=self.params['rsi_window']) # add rsi info to portvals
        if(self.verbose): plot_data(portvals['RSI'])

        # CREATE STRATEGY
        # buy stock when current price is lower than the bollinger low band and the price is higher than the rsi_buy_threshold, 
        # keep track of open positions, and limit to x
        # sell stock if open order reaches take profit level or stop loss
        for date, row in portvals.iterrows():
            if(np.isnan(row['Moving Avg'])):
                continue
            if(np.isnan(row['RSI'])):
                continue

            # buy guard
            b_buy = row[name] < row['Bollinger Lower']
            rsi_buy = row['RSI'] > self.params['rsi_buy_threshold']
            buy = b_buy and rsi_buy

            # place buy order
            if (buy and (len(self.positions) < self.params['max_positions'])):
                if(self.verbose):print(f'open long at {row[name]}')
                self.place_order(row[name], date, name, 'BUY', shares_per_trade)

            # check stop loss and take profit for all positions
            for p in self.positions:
                if (self.take_profit_met(p,row[name], self.params['take_profit_%'])):
                    if(self.verbose):print(f'take profit triggered at {row[name]}')
                    self.place_order(p, date, name, 'SELL', shares_per_trade)
                elif (self.stop_loss_met(p,row[name], self.params['stop_loss_%'])):
                    if(self.verbose):print(f'stop loss triggered at {row[name]}')
                    self.place_order(p, date, name, 'SELL', shares_per_trade)

        return self.order_book