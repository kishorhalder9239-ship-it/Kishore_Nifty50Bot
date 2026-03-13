import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"]

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })


def get_klines(symbol):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 5
    }

    r = requests.get(url, params=params)

    return r.json()


def check_pattern(symbol):

    data = get_klines(symbol)

    if len(data) < 5:
        return

    c1 = data[-4]
    c2 = data[-3]
    c3 = data[-2]

    o1 = float(c1[1])
    cl1 = float(c1[4])

    o2 = float(c2[1])
    cl2 = float(c2[4])

    o3 = float(c3[1])
    cl3 = float(c3[4])

    body1 = abs(cl1-o1)
    body2 = abs(cl2-o2)

    # big → small → same direction

    if body2 < body1 * 0.5:

        if cl1 > o1 and cl3 > o3:

            send_message(f"BUY SIGNAL {symbol}")

        elif cl1 < o1 and cl3 < o3:

            send_message(f"SELL SIGNAL {symbol}")


print("BOT RUNNING")

while True:

    for symbol in symbols:

        print("checking", symbol)

        check_pattern(symbol)

        time.sleep(2)

    time.sleep(30)
