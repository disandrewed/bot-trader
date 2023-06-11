from datetime import datetime, timedelta
import yfinance as yf
import pandas_ta as ta
import time as timer

# asset class
class MyAsset:
    def __init__(self, name):
        self.ticker = name
        self.holding = False
        self.getter = yf.Ticker(name)
        

# asset list
asset_list = ["AMZN", "AAPL", "GOOG"]

asset_class_list = []
for asset_name in asset_list:
    print("creating asset for: " + asset_name)
    ass = MyAsset(asset_name)
    asset_class_list.append(ass)
    

while True:
    for asset in asset_class_list:
        #start_date = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
        df = asset.getter.history(period='1d', interval='1m', actions=False)

        print()
        print(asset.ticker)
        print(df.tail(5))

        df['ma_fast'] = ta.sma(df['Close'], 10)
        df['ma_slow'] = ta.sma(df['Close'], 30)
        
        
        price = df.iloc[-1]['Close']
        
        if df.iloc[-1]['ma_fast'] > df.iloc[-1]['ma_slow'] and not asset.holding:
            print("buy " + asset.ticker + "at price: " + price)
            asset.holding = True
        elif df.iloc[-1]['ma_fast'] < df.iloc[-1]['ma_slow'] and asset.holding:
            print("sell " + asset.ticker + "at price: " + price)
            asset.holding = False
    print("\nwaiting...")
    timer.sleep(60)