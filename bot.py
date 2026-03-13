import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbol = "BTCUSDT"
last_candle = None


def send(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass


def get_candle():
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": "1m", "limit": 3}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if isinstance(data, list) and len(data) >= 3:
            return data[-2]
        else:
            return None

    except:
        return None


print("BOT STARTED")

while True:

    candle = get_candle()

    if candle:

        candle_time = candle[0]

        if candle_time != last_candle:

            last_candle = candle_time

            open_price = float(candle[1])
            close_price = float(candle[4])

            if close_price > open_price:
                send(f"BUY SIGNAL {symbol}")
            else:
                send(f"SELL SIGNAL {symbol}")

            print("Signal sent")

    time.sleep(5)
