import os
import requests
import json
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from colorama import init, Fore, Style

init()

class CryptoTracker:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"
        self.api_secret = "YOUR_API_SECRET"
        self.api_base = "https://api.binance.com/api/v3"
        self.cryptos = ["BTCUSDT", "ETHUSDT", "LTCUSDT", "BNBUSDT", "XRPUSDT"]

    def get_price(self, symbol):
        url = f"{self.api_base}/ticker/price?symbol={symbol}"
        headers = {"X-MBX-APIKEY": self.api_key, "X-MBX-SECRET-KEY": self.api_secret}
        response = requests.get(url, headers=headers)
        return response.json()["price"]

    def get_historical_data(self, symbol, interval, limit):
        url = f"{self.api_base}/klines?symbol={symbol}&interval={interval}&limit={limit}"
        headers = {"X-MBX-APIKEY": self.api_key, "X-MBX-SECRET-KEY": self.api_secret}
        response = requests.get(url, headers=headers)
        return response.json()

    def plot_price(self, symbol, interval, limit):
        data = self.get_historical_data(symbol, interval, limit)
        df = pd.DataFrame(data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote Asset Volume", "Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Can Be Ignored"])
        df["Date"] = pd.to_datetime(df["Open Time"], unit="ms")
        df.set_index("Date", inplace=True)
        plt.figure(figsize=(12,6))
        plt.plot(df["Close"])
        plt.title(f"{symbol} Price Chart")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()

    def track_crypto(self):
        for symbol in self.cryptos:
            price = self.get_price(symbol)
            print(f"{symbol}: ${price}")

    def track_crypto_historical(self, symbol, interval, limit):
        data = self.get_historical_data(symbol, interval, limit)
        df = pd.DataFrame(data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote Asset Volume", "Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Can Be Ignored"])
        df["Date"] = pd.to_datetime(df["Open Time"], unit="ms")
        df.set_index("Date", inplace=True)
        print(df)

def main():
    tracker = CryptoTracker()
    while True:
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Track all cryptos")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Track historical data for a crypto")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Plot price chart for a crypto")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            tracker.track_crypto()
        elif choice == "2":
            symbol = input("Enter the symbol: ")
            interval = input("Enter the interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M): ")
            limit = int(input("Enter the limit: "))
            tracker.track_crypto_historical(symbol, interval, limit)
        elif choice == "3":
            symbol = input("Enter the symbol: ")
            interval = input("Enter the interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M): ")
            limit = int(input("Enter the limit: "))
            tracker.plot_price(symbol, interval, limit)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()