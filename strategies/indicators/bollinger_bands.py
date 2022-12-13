def bollinger_bands_indicator(portvals, name, window=20):
    # add bollinger indicator details
    # add a moving average, upper bollinger band and lower bolinger band to portvals
    portvals['Moving Avg'] = portvals[name].rolling(window).mean()
    portvals['Bollinger Upper'] = portvals[name].rolling(window).mean() + (2* portvals[name].rolling(window).std())
    portvals['Bollinger Lower'] = portvals[name].rolling(window).mean() - (2* portvals[name].rolling(window).std())
    return portvals
