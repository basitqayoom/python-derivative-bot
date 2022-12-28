from datetime import datetime 
from websocket import WebSocketApp

from functions import *

# Define trade function
def driver_code(condition=True):
  symbol = "BTCUSDT"
  interval = "1m"
  # from index import driver_code
  
  # Miniticker for server
  asset = "btcusdt"
  websocket_endpoint = f"wss://stream.binance.com:9443/ws/{asset}@miniTicker"
 
  # Define a callback function to handle the WebSocket connection being closed
  def on_error(ws, error):
    print(error)
    
  def on_close(ws,error):
    if error is not None:
        # Print the error message if an error occurred
        print(f"WebSocket connection closed with error: {error}")
    else:
        print("In close")
        print("WebSocket connection closed")   
    
  def on_message(ws,message):
    from trade import trade
    # Parse the message as JSON
    data = json.loads(message)
    
    # Extract the serverTime field from the message
    server_time = int(data['E'])
    timestamp_seconds = server_time / 1000
    
    # Convert the timestamp to a UTC time using the datetime.utcfromtimestamp() function
    utc_time = datetime.utcfromtimestamp(timestamp_seconds)
    
    # Convert the UTC time to a string in the format "SS"
    seconds = utc_time.strftime("%S")
    print(seconds)
    if seconds == "59":
      # Print a message if the WebSocket connection was closed normally
      close_prices, rsi_values = get_price_and_rsi(symbol, interval)
      signal = generate_signal(close_prices, rsi_values)
      if signal != "HOLD" :
        print(f"Trading signal for {interval}: {signal}")
        # Get the current UTC time
        utc_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        trade(symbol,interval,signal,float(close_prices[0]),utc_time)
        ws.close()
      print("No Divergence found")  

  try:                    
    # Create the WebSocket connection
    ws = WebSocketApp(websocket_endpoint, on_message=on_message, on_close=on_close, on_error=on_error)
    # Run the event loop to receive data from the WebSocket connection
    ws.run_forever()
  except Exception as e:
    print(e)  

driver_code()