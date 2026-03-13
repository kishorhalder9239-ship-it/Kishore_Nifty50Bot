import requests
import time

symbols = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"]

def get_klines(symbol):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 6
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except:
        return []

def check_pattern(symbol):

    data = get_klines(symbol)

    if len(data) < 6:
        return

    # last CLOSED candles
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

    print(symbol,"b1:",body1,"b2:",body2)

    # big → small → same direction
    if body2 < body1:

        if cl1 > o1 and cl3 > o3:
            print("BUY PATTERN FOUND",symbol)

        elif cl1 < o1 and cl3 < o3:
            print("SELL PATTERN FOUND",symbol)


print("BOT RUNNING")

while True:

    for s in symbols:
        check_pattern(s)
        time.sleep(1)

    time.sleep(20)
