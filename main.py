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
asset_list = ["AMZN"]
asset_class_list = []
for asset_name in asset_list:
    print("creating asset for: " + asset_name)
    ass = MyAsset(asset_name)
    asset_class_list.append(ass)
    

while True:
    for asset in asset_class_list:
        start_date = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
        df = asset.getter.history(start=start_date, interval='1m')

        print(asset.ticker)
        print(df.tail(5))
        del df['Dividends']
        del df['Stock Splits']
        del df['Volume']
        df['SMA_fast'] = ta.sma(df['Close'], 10)
        df['SMA_slow'] = ta.sma(df['Close'], 30)
        
        
        
        price = df.iloc[-1]['Close']
        if df.iloc[-1]['SMA_fast'] > df.iloc[-1]['SMA_slow'] and not asset.holding:
            print("buy " + asset.ticker)
            df.holding = True
        elif df.iloc[-1]['SMA_fast'] < df.iloc[-1]['SMA_slow'] and asset.holding:
            print("sell " + asset.ticker)
    print("waiting...")
    timer.sleep(60)