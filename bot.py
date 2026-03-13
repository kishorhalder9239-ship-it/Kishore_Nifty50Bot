import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})


def get_candle(symbol):

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":symbol,
        "interval":"1m",
        "limit":2
    }

    r=requests.get(url,params=params)

    data=r.json()

    return data


def check(symbol):

    data=get_candle(symbol)

    if not isinstance(data,list):
        return

    candle=data[-2]

    open_price=float(candle[1])
    close_price=float(candle[4])

    if close_price>open_price:

        send(f"BUY SIGNAL {symbol}")

    else:

        send(f"SELL SIGNAL {symbol}")


print("BOT STARTED")

while True:

    for s in symbols:

        print("checking",s)

        check(s)

        time.sleep(1)

    time.sleep(30)
