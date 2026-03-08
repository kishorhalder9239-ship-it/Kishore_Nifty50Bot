import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

TP_PERCENT = 0.25
SL_PERCENT = 0.15

symbols = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","DOGEUSDT","AVAXUSDT","TRXUSDT","DOTUSDT"
]

active_trades = {}
wins = 0
losses = 0
total_signals = 0


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url,data={"chat_id":CHAT_ID,"text":text},timeout=10)
    except:
        pass


def get_klines(symbol):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol":symbol,
        "interval":"5m",
        "limit":3
    }

    try:
        return requests.get(url,params=params,timeout=10).json()
    except:
        return []


def get_price(symbol):

    url = "https://api.binance.com/api/v3/ticker/price"

    try:
        return float(requests.get(url,params={"symbol":symbol}).json()["price"])
    except:
        return None


def check_pattern(symbol):

    global total_signals

    data = get_klines(symbol)

    if len(data) < 3:
        return

    c1,c2,c3 = data

    o1,cl1 = float(c1[1]),float(c1[4])
    o2,cl2 = float(c2[1]),float(c2[4])
    o3,cl3 = float(c3[1]),float(c3[4])

    body1 = abs(cl1-o1)
    body2 = abs(cl2-o2)
    body3 = abs(cl3-o3)


    if body2 < body1 and body2 < body3:

        entry = cl3

        if cl1>o1 and cl3>o3:

            direction = "BUY"
            tp = entry*(1+TP_PERCENT/100)
            sl = entry*(1-SL_PERCENT/100)

        elif cl1<o1 and cl3<o3:

            direction = "SELL"
            tp = entry*(1-TP_PERCENT/100)
            sl = entry*(1+SL_PERCENT/100)

        else:
            return


        active_trades[symbol] = {
            "direction":direction,
            "entry":entry,
            "tp":tp,
            "sl":sl
        }

        total_signals += 1

        send_message(f"""
🚀 BigSmallBig SIGNAL

Symbol: {symbol}
Type: {direction}

Entry: {entry}
TP: {round(tp,4)}
SL: {round(sl,4)}

Total Signals: {total_signals}
""")


def check_results():

    global wins,losses

    for symbol in list(active_trades.keys()):

        price = get_price(symbol)

        if not price:
            continue

        trade = active_trades[symbol]

        if trade["direction"]=="BUY":

            if price>=trade["tp"]:

                wins +=1
                send_message(f"✅ TP HIT {symbol}\nWins: {wins} Losses: {losses}")
                del active_trades[symbol]

            elif price<=trade["sl"]:

                losses +=1
                send_message(f"❌ SL HIT {symbol}\nWins: {wins} Losses: {losses}")
                del active_trades[symbol]


        if trade["direction"]=="SELL":

            if price<=trade["tp"]:

                wins +=1
                send_message(f"✅ TP HIT {symbol}\nWins: {wins} Losses: {losses}")
                del active_trades[symbol]

            elif price>=trade["sl"]:

                losses +=1
                send_message(f"❌ SL HIT {symbol}\nWins: {wins} Losses: {losses}")
                del active_trades[symbol]


print("BigSmallBig Scanner Started")


while True:

    for symbol in symbols:

        print("Scanning",symbol)

        check_pattern(symbol)

        time.sleep(1)

    check_results()

    time.sleep(60)
