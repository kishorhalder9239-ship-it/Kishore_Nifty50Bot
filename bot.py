import os
import time
import requests
import yfinance as yf
import pandas as pd

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

def check_signal(symbol):
    data = yf.download(symbol, period="1d", interval="5m")
    
    if len(data) < 3:
        return
    
    last = data.iloc[-1]
    prev = data.iloc[-2]

    # Big-Small-Big logic simple demo
    body1 = abs(prev['Close'] - prev['Open'])
    body2 = abs(last['Close'] - last['Open'])

    if body2 > body1 * 1.2:
        direction = "BUY 🚀" if last['Close'] > last['Open'] else "SELL 🔻"
        
        entry = round(last['Close'], 4)
        tp = round(entry * 1.003, 4)
        sl = round(entry * 0.998, 4)

        message = f"""
🚀 BIGSMALLBIG ALERT

Symbol: {symbol}
Timeframe: 5m
Direction: {direction}
Entry: {entry}
TP: {tp}
SL: {sl}
"""
        send_message(message)

def main():
    send_message("🔥 Bot Cloud Mode Started")

    symbols = ["BTC-USD", "ETH-USD", "SOL-USD"]

    while True:
        for symbol in symbols:
            try:
                check_signal(symbol)
            except Exception as e:
                print("Error:", e)
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    main()
