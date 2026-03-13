import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"]

def send(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})


def get_candles(symbol):

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":symbol,
        "interval":"1m",
        "limit":5
    }

    return requests.get(url,params=params).json()


def check(symbol):

    data=get_candles(symbol)

    c1=data[-4]
    c2=data[-3]
    c3=data[-2]

    o1=float(c1[1]); c1c=float(c1[4])
    o2=float(c2[1]); c2c=float(c2[4])
    o3=float(c3[1]); c3c=float(c3[4])

    body1=abs(c1c-o1)
    body2=abs(c2c-o2)

    # BIG → SMALL → SAME DIRECTION

    if body2 < body1*0.8:

        if c1c>o1 and c3c>o3:

            send(f"BUY SIGNAL {symbol}")

        elif c1c<o1 and c3c<o3:

            send(f"SELL SIGNAL {symbol}")


print("BOT STARTED")

while True:

    for s in symbols:

        print("checking",s)

        check(s)

        time.sleep(1)

    time.sleep(60)
