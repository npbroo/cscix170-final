import numpy as np
from scipy.optimize import minimize, fmin
from marketsim import calculate_profit

TICKER = 'SPY'
START_DATE = '2000-02-10'
END_DATE = '2012-06-10'
START_VAL = 100000

def objective_fcn(parameters):
    profit = calculate_profit(TICKER, START_DATE, END_DATE, START_VAL, parameters)
    print(profit)
    return -profit

bounds_bollinger_window = (5,25)
rsi_window = (5,25)
rsi_lower = (1,100)
rsi_upper = (1,100)
max_positions = (1,10)
take_profit = (.01,.5)
stop_loss = (0,.5)

bounds = [
    bounds_bollinger_window, 
    rsi_window, 
    rsi_lower, 
    rsi_upper, 
    max_positions, 
    take_profit, 
    stop_loss
]

# intial values
x0 = [
    9,      #bollinger_window
    14,     #rsi_window
    42,     #rsi_lower
    70,     #rsi_upper
    3,       #max_positions 
    0.15,   #take_profit
    0.03,    #stop_loss
]

result = fmin(objective_fcn, x0, bounds=bounds, method='SLSQP', tol="2")
print(result)


