import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","DOGEUSDT","AVAXUSDT","TRXUSDT","DOTUSDT"
]

def send(text):

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id":CHAT_ID,
        "text":text
    })


def get_data(symbol):

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":symbol,
        "interval":"1m",   # 👈 1 minute candle
        "limit":5
    }

    r=requests.get(url,params=params)

    return r.json()


def scan():

    for s in symbols:

        d=get_data(s)

        o1=float(d[-4][1])
        c1=float(d[-4][4])

        o2=float(d[-3][1])
        c2=float(d[-3][4])

        o3=float(d[-2][1])
        c3=float(d[-2][4])

        b1=abs(c1-o1)
        b2=abs(c2-o2)
        b3=abs(c3-o3)

        print(s,b1,b2,b3)

        if b2<b1 and b2<b3:

            send
