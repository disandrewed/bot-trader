from datetime import datetime, timedelta
import yfinance as yf
import pandas_ta as ta
import time as timer

# asset class
class MyAsset:
    def __init__(self, name):
        self.ticker = name
        self.holding = False
        self.value = 0
        self.getter = yf.Ticker(name)

# asset list
asset_list = ["AUDUSD=X"]
amount = 0

# create class list using assets provided
asset_class_list = []
for asset_name in asset_list:
    print("creating asset for: " + asset_name)
    ass = MyAsset(asset_name)
    asset_class_list.append(ass)
    
# loop infinitely constantly getting updated information and determining buy/sell
while True:
    for asset in asset_class_list:
        # start_date = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
        # df = asset.getter.history(start=start_date, interval='1m', actions=False)
        df = asset.getter.history(period='1d', interval='1m', actions=False)

        print()
        print(asset.ticker)
        print(df.tail(5))

        df['ma_fast'] = ta.sma(df['Close'], 10)
        df['ma_slow'] = ta.sma(df['Close'], 30)
        
        price = df.iloc[-1]['Close']
        if df.iloc[-1]['ma_fast'] > df.iloc[-1]['ma_slow'] and not asset.holding:
            print("buy " + asset.ticker + " at price: " + str(price))
            asset.holding = True
            asset.value = price
            amount -= price
        elif df.iloc[-1]['ma_fast'] < df.iloc[-1]['ma_slow'] and asset.holding and price > asset.value:
            print("sell " + asset.ticker + " at price: " + str(price))
            asset.holding = False
            asset.price = 0
            amount += price

    print("\nbank acc: " + str(amount))    
    print("waiting...")
    timer.sleep(10)