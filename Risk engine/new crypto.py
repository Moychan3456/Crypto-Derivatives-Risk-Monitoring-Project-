import yfinance as cx
import pandas as pd

btc = cx.download("BTC-USD", period="30d", interval="1h")
eth = cx.download("ETH-USD", period="30d", interval="1h")

btc.to_csv("btc_prices.csv")
eth.to_csv("eth_prices.csv")
