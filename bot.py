import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"]

def send(msg):

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url,data={"chat_id":CHAT_ID,"text":msg})
    except:
        pass


def get_candles(symbol):

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":symbol,
        "interval":"1m",
        "limit":50
    }

    r=requests.get(url,params=params)

    data=r.json()

    closes=[float(x[4]) for x in data]

    return closes


def ema(data,period):

    k=2/(period+1)

    ema_val=data[0]

    for price in data:

        ema_val=price*k+ema_val*(1-k)

    return ema_val


def check(symbol):

    closes=get_candles(symbol)

    ema9=ema(closes[-9:],9)

    ema21=ema(closes[-21:],21)

    price=closes[-1]

    if ema9>ema21:

        send(f"BUY SIGNAL {symbol} price:{price}")

    elif ema9<ema21:

        send(f"SELL SIGNAL {symbol} price:{price}")


print("BOT RUNNING")

while True:

    for s in symbols:

        print("checking",s)

        check(s)

        time.sleep(1)

    time.sleep(60)
