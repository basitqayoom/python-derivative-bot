import json
from websocket import WebSocketApp
import datetime

from googleSheets import addData

# Define trade function
def trade(symbol, interval, signal, buy_price, buy_time):  
  
  # from index import driver_code
  asset = symbol.lower()
  websocket_endpoint = f"wss://stream.binance.com:9443/ws/{asset}@ticker"
  


  # Define a callback function to handle the WebSocket connection being closed
  def on_close(ws,error):
    from driver import driver_code
    print("In error")
    if error is not None:
        # Print the error message if an error occurred
        print(f"WebSocket connection closed with error: {error}")
    else:
        # Print a message if the WebSocket connection was closed normally
        
        print("WebSocket connection closed")   
    
  def on_message(ws,message):
    print("Trading now")
    
    # Parse the message using the json library
    data = json.loads(message)
    # Extract the data from the message
    price = float(data["c"])
    pos_open_time = buy_time
    pos_open_price = float(buy_price)
    pos_close_price = price
    TP = 0.002
    SL = 0.008
    
    print(buy_price,price)  
    # Check signal
    # Buy Long
    if signal == 'BUY':
      # Open position on Binance Futures
      # ----------Code here------------------  
      
      # Check for price to hit TP or SL
      # TP
      if price >= (buy_price + TP*buy_price):
        # Add data to spreadsheet
        # -------------Code here-----------------
        try:
            pos_close_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            addData(signal, symbol, interval, pos_open_time, pos_open_price, pos_close_time, pos_close_price)
        except Exception as e:
            # handle the exception
            print(f"Error adding data to spreadsheet: {e}")
        finally:
            ws.close()
            # driver_code(True)
      # SL
      elif price <= (buy_price - SL*buy_price):
        # Add data to spreadsheet
        # -------------Code here-----------------
        try:
            pos_close_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            addData(signal, symbol, interval, pos_open_time, pos_open_price, pos_close_time, pos_close_price)
        except Exception as e:
            # handle the exception
            print(f"Error adding data to spreadsheet: {e}")
        finally:
            ws.close()
            # driver_code(True)
    
    elif signal == 'SELL':
      # Open position on Binance Futures
      # ----------Code here------------------
      
      # Check for price to hit TP or SL
      # TP
      if price <= (buy_price - TP*buy_price):
        # Add data to spreadsheet
        # -------------Code here-----------------
        try:
            pos_close_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            addData(signal, symbol, interval, pos_open_time, pos_open_price, pos_close_time, pos_close_price)
        except Exception as e:
            # handle the exception
            print(f"Error adding data to spreadsheet: {e}")
        finally:
            ws.close()
            # driver_code(True)
      # SL
      elif price >= (buy_price + SL*buy_price):
        # Add data to spreadsheet
        # -------------Code here-----------------
        try:
            pos_close_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            addData(signal, symbol, interval, pos_open_time, pos_open_price, pos_close_time, pos_close_price)
        except Exception as e:
            # handle the exception
            print(f"Error adding data to spreadsheet: {e}")
        finally:
            ws.close()
            # driver_code(True)  
  try:                    
    # Create the WebSocket connection
    ws = WebSocketApp(websocket_endpoint, on_message=on_message, on_close=on_close)
    # Run the event loop to receive data from the WebSocket connection
    ws.run_forever()
  except Exception as e:
    print(e)  

            
