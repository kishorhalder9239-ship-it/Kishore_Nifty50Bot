import requests
import time
import datetime

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

TP_PERCENT = 0.25
SL_PERCENT = 0.15

symbols = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","DOGEUSDT","AVAXUSDT","TRXUSDT","DOTUSDT",
"MATICUSDT","LTCUSDT","BCHUSDT","LINKUSDT","XLMUSDT",
"ATOMUSDT","ETCUSDT","FILUSDT","APTUSDT","NEARUSDT",
"HBARUSDT","VETUSDT","OPUSDT","ARBUSDT","INJUSDT",
"SUIUSDT","SEIUSDT","AAVEUSDT","GRTUSDT","ALGOUSDT",
"SANDUSDT","MANAUSDT","AXSUSDT","EGLDUSDT","THETAUSDT",
"XTZUSDT","FLOWUSDT","KAVAUSDT","CHZUSDT","FTMUSDT",
"RNDRUSDT","DYDXUSDT","GMXUSDT","BLURUSDT","COMPUSDT",
"ZECUSDT","KSMUSDT","SNXUSDT","CRVUSDT","LDOUSDT",
"RUNEUSDT","STXUSDT","MINAUSDT","PEPEUSDT","SHIBUSDT",
"1000BONKUSDT","FLOKIUSDT","WLDUSDT","PYTHUSDT","JUPUSDT"
]

active_trades = {}
wins = 0
losses = 0


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
        "limit":60
    }

    try:
        return requests.get(url,params=params,timeout=10).json()
    except:
        return []


def build_candle(c):

    o = float(c[0][1])
    cl = float(c[-1][4])

    highs = [float(x[2]) for x in c]
    lows = [float(x[3]) for x in c]

    h = max(highs)
    l = min(lows)

    return o,h,l,cl


def check_pattern(symbol,data,size,timeframe):

    if len(data) < size*4:
        return

    c1 = build_candle(data[-size*4:-size*3])
    c2 = build_candle(data[-size*3:-size*2])
    c3 = build_candle(data[-size*2:-size])

    o1,h1,l1,cl1 = c1
    o2,h2,l2,cl2 = c2
    o3,h3,l3,cl3 = c3

    body1 = abs(cl1-o1)
    body2 = abs(cl2-o2)
    body3 = abs(cl3-o3)

    if body2 < body1 and body2 < body3:

        if cl1 > o1 and cl3 > o3:
            direction="BUY"

        elif cl1 < o1 and cl3 < o3:
            direction="SELL"

        else:
            return

        entry = cl3

        if direction=="BUY":

            tp = entry*(1+TP_PERCENT/100)
            sl = entry*(1-SL_PERCENT/100)

        else:

            tp = entry*(1-TP_PERCENT/100)
            sl = entry*(1+SL_PERCENT/100)

        active_trades[symbol] = {
            "direction":direction,
            "entry":entry,
            "tp":tp,
            "sl":sl
        }

        send_message(f"""
🚀 SIGNAL

Symbol: {symbol}
Type: {direction}
Timeframe: {timeframe}

Entry: {entry}
TP: {tp}
SL: {sl}
""")


def scan_market():

    for symbol in symbols:

        print("Scanning",symbol)

        data = get_klines(symbol)

        if not data:
            continue

        check_pattern(symbol,data,1,"5m")
        check_pattern(symbol,data,3,"15m")
        check_pattern(symbol,data,6,"30m")
        check_pattern(symbol,data,12,"1h")

        time.sleep(0.5)


def check_results():

    global wins,losses

    for symbol in list(active_trades.keys()):

        try:

            price = float(
                requests.get(
                    "https://api.binance.com/api/v3/ticker/price",
                    params={"symbol":symbol},
                    timeout=10
                ).json()["price"]
            )

        except:
            continue

        trade = active_trades[symbol]

        if trade["direction"]=="BUY":

            if price>=trade["tp"]:

                wins+=1
                send_message(f"✅ TP HIT {symbol}\nWins:{wins} Loss:{losses}")
                del active_trades[symbol]

            elif price<=trade["sl"]:

                losses+=1
                send_message(f"❌ SL HIT {symbol}\nWins:{wins} Loss:{losses}")
                del active_trades[symbol]

        else:

            if price<=trade["tp"]:

                wins+=1
                send_message(f"✅ TP HIT {symbol}\nWins:{wins} Loss:{losses}")
                del active_trades[symbol]

            elif price>=trade["sl"]:

                losses+=1
                send_message(f"❌ SL HIT {symbol}\nWins:{wins} Loss:{losses}")
                del active_trades[symbol]


def wait_for_next_candle():

    now = datetime.datetime.utcnow()

    seconds = now.minute*60 + now.second

    wait = 300 - (seconds % 300)

    print(f"⏳ Waiting {wait} sec for next 5m candle")

    time.sleep(wait)


print("🔥 BOT STARTED")


while True:

    try:

        wait_for_next_candle()

        print("📊 Scanning market...")

        scan_market()

        check_results()

        print("✅ Scan finished")

    except Exception as e:

        print("❌ ERROR:",e)

        time.sleep(10)
