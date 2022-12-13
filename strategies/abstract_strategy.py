from abc import abstractmethod

# Abstract class to create a basic strategy with common helper methods
class Strategy():
    # default parameters for the strategy
    verbose = False
    default_params = {}
    order_book = []
    positions = []

    def __init__(self, default_params, verbose=False):
        self.verbose = verbose
        self.default_params = default_params

    def set_verbose(self, verbose):
        self.verbose = verbose

    # insert default required parameters into passed params if they dont exist
    def load_parameters(self, params):
        for key in self.default_params:
            if (not key in params): params[key] = self.default_params[key]
        return params

    # adds either a buy or sell order to the order book
    def place_order(self, position, date, ticker, type, amount):
        if(type == 'BUY'):
            self.positions.append(position)
        elif(type == 'SELL'):
            self.positions.remove(position)
        self.order_book.append({'Date':date, 'Symbol':ticker, 'Order':type, 'Shares':amount})

    # checks if the stop loss is met
    def stop_loss_met(self, position, current_price, stop_loss):
        if((position/current_price)-1 >= stop_loss):
            return True
        return False

    # checks if the take profit has been met
    def take_profit_met(self, position, current_price, take_profit):
        if((current_price/position)-1 >= take_profit):
            return True
        return False

    @abstractmethod
    def run_strategy(self, portvals, name, shares_per_trade):
        pass