import gspread


# Use the service account key to authenticate
sa = gspread.service_account(filename="python-trading-372511-9fa05d53f32b.json")
sh = sa.open("Backtesting-BOT")
wks = sh.worksheet("backtest")

def addData(signal,symbol, interval, position_open_time, position_open_price, position_close_time, position_close_price):
    net_profit = float(position_close_price) - float(position_open_price) if signal == "BUY" else float(position_open_price) - float(position_close_price) 
    net_profit_percent = (net_profit/float(position_open_price))*100
    p_or_l = "P" if net_profit>=0 else "L"
    row = [symbol.upper(), interval, position_open_time, position_open_price, position_close_time, position_close_price, net_profit_percent, p_or_l,signal]
    
    wks.add_rows(1)
    num = wks.row_count+1
    red = 0.8 if net_profit < 0 else 0
    green = 0.8 if net_profit >= 0 else 0
    wks.format(f"{num}:{num}", {
    "backgroundColor": {
      "red": red,
      "green": green,
      "blue": 0.0
    }})
    wks.append_row(values= row)
    print("Data successfully added to G-Sheet")
    
    from driver import driver_code
    driver_code()
    

    
            