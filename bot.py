import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = [
"BTCUSDT",
"ETHUSDT",
"BNBUSDT",
"SOLUSDT",
"XRPUSDT"
]


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        }, timeout=10)
    except:
        pass


def get_candles(symbol):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 3
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except:
        return []


def check_engulfing(symbol):

    data = get_candles(symbol)

    if len(data) < 3:
        return


    prev = data[-2]
    last = data[-1]


    o1 = float(prev[1])
    c1 = float(prev[4])

    o2 = float(last[1])
    c2 = float(last[4])


    print(symbol, o1, c1, o2, c2)


    # Bullish Engulfing
    if c1 < o1 and c2 > o2 and c2 > o1 and o2 < c1:

        send_message(f"BUY SIGNAL {symbol}")


    # Bearish Engulfing
    if c1 > o1 and c2 < o2 and c2 < o1 and o2 > c1:

        send_message(f"SELL SIGNAL {symbol}")


print("BOT STARTED")


while True:

    for symbol in symbols:

        print("Scanning", symbol)

        check_engulfing(symbol)

        time.sleep(1)

    print("Waiting next scan")

    time.sleep(60)
