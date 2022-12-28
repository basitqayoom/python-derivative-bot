import requests
import json
import numpy as np
import pandas_ta as ta
import pandas as pd

# Function to retrieve price and RSI data from Binance
def get_price_and_rsi(symbol, interval):
  params = { "symbol": symbol, "interval": interval, "limit": 1000 }
  response = requests.get("https://api.binance.com/api/v3/klines", params=params)
  data = json.loads(response.text)
  close_prices = [float(d[4]) for d in data]
  close_prices = np.array(close_prices)
  series = pd.Series(close_prices)
  rsi_values = ta.rsi(series)
  rsi_values = rsi_values.tolist()
  close_prices = np.flip(close_prices)
  close_prices = close_prices[0:15]
  rsi_values= np.flip(rsi_values)
  rsi_values = rsi_values[0:15]
  return close_prices, rsi_values

# Function to generate signals
def generate_signal(close_prices, rsi_values):
  for i in range(0,13):
      if close_prices[0] < close_prices[i+2] and rsi_values[0] > rsi_values[i+2]:
        return "BUY"
      elif close_prices[0] > close_prices[i+2] and rsi_values[0] < rsi_values[i+2]:
        return "SELL"
  return "HOLD"

