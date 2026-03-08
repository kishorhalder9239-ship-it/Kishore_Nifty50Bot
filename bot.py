import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","DOGEUSDT","AVAXUSDT","TRXUSDT","DOTUSDT"
]

def send(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url,data={"chat_id":CHAT_ID,"text":text})
    except:
        pass


def check(symbol):

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":symbol,
        "interval":"1m",
        "limit":4
    }

    try:
        data=requests.get(url,params=params).json()
    except:
        return


    o1=float(data[-4][1])
    c1=float(data[-4][4])

    o2=float(data[-3][1])
    c2=float(data[-3][4])

    o3=float(data[-2][1])
    c3=float(data[-2][4])


    b1=abs(c1-o1)
    b2=abs(c2-o2)
    b3=abs(c3-o3)

    print(symbol,b1,b2,b3)


    # Big Small Big
    if b2 < b1*0.7 and b2 < b3*0.7:

        if c1>o1 and c3>o3:

            send(f"BUY pattern {symbol}")

        elif c1<o1 and c3<o3:

            send(f"SELL pattern {symbol}")


print("BOT STARTED")

while True:

    for s in symbols:

        check(s)

        time.sleep(0.2)

    print("scan done")

    time.sleep(60)
