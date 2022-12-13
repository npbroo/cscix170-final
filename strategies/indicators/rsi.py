def rsi_indicator(portvals, name, window=14):
    # rsi indicator
    close_delta = portvals[name].diff()
    up = close_delta.clip(lower=0)
    down = -1*close_delta.clip(upper=0)
    ma_up = up.rolling(window=window).mean()
    ma_down = down.rolling(window=window).mean()
    rsi = ma_up/ma_down
    rsi = 100 - (100/(1+rsi))
    portvals['RSI'] = rsi 
    return portvals