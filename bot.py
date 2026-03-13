import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbol = "BTCUSDT"

def send(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url,data={"chat_id":CHAT_ID,"text":msg})
    except:
        pass


def get_candle():

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 2
    }

    r = requests.get(url,params=params)

    data = r.json()

    return data[-2]


print("BOT STARTED")

while True:

    candle = get_candle()

    open_price = float(candle[1])
    close_price = float(candle[4])

    if close_price > open_price:

        send(f"BUY SIGNAL {symbol}")

    else:

        send(f"SELL SIGNAL {symbol}")

    time.sleep(60)
