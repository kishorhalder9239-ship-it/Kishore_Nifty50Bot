import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"
]

def send(msg):

    try:
        url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(url,data={
            "chat_id":CHAT_ID,
            "text":msg
        },timeout=10)

    except Exception as e:
        print("telegram error",e)


def check(symbol):

    try:

        url="https://api.binance.com/api/v3/klines"

        params={
            "symbol":symbol,
            "interval":"1m",
            "limit":4
        }

        data=requests.get(url,params=params,timeout=10).json()

    except Exception as e:

        print("api error",symbol,e)

        return


    try:

        o1=float(data[-4][1])
        c1=float(data[-4][4])

        o2=float(data[-3][1])
        c2=float(data[-3][4])

        o3=float(data[-2][1])
        c3=float(data[-2][4])

    except:
        return


    b1=abs(c1-o1)
    b2=abs(c2-o2)
    b3=abs(c3-o3)

    print(symbol,b1,b2,b3)


    if b2 < b1*0.7 and b2 < b3*0.7:

        if c1>o1 and c3>o3:

            send(f"BUY pattern {symbol}")

        elif c1<o1 and c3<o3:

            send(f"SELL pattern {symbol}")


print("BOT STARTED")


while True:

    try:

        for s in symbols:

            print("Scanning",s)

            check(s)

            time.sleep(1)   # API safe

        print("Scan finished")

        time.sleep(60)

    except Exception as e:

        print("main loop error",e)

        time.sleep(10)
