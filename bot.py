import requests
import time
import datetime

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

TP_PERCENT = 0.25
SL_PERCENT = 0.15

symbols = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","DOGEUSDT","TRXUSDT","AVAXUSDT","DOTUSDT",
"MATICUSDT","LINKUSDT","LTCUSDT","ATOMUSDT","UNIUSDT",
"ETCUSDT","FILUSDT","APTUSDT","ARBUSDT","OPUSDT",
"NEARUSDT","SANDUSDT","MANAUSDT","AAVEUSDT","ALGOUSDT",
"FTMUSDT","EOSUSDT","XTZUSDT","EGLDUSDT","THETAUSDT",
"AXSUSDT","FLOWUSDT","CHZUSDT","GALAUSDT","DYDXUSDT",
"CRVUSDT","SNXUSDT","1INCHUSDT","KAVAUSDT","ROSEUSDT",
"LDOUSDT","GMTUSDT","IMXUSDT","APEUSDT","RUNEUSDT",
"KSMUSDT","ZILUSDT","ENSUSDT","COMPUSDT","SUSHIUSDT",
"BATUSDT","CELOUSDT","QTUMUSDT","ANKRUSDT","IOTAUSDT",
"RVNUSDT","ICXUSDT","HOTUSDT","ONTUSDT","STXUSDT"
]

last_signal = {}
active_trades = {}

wins = 0
losses = 0
signals_today = 0

start_time = datetime.datetime.now()


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        requests.post(url, data=data)
    except:
        pass


def get_klines(symbol):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "5m",
        "limit": 50
    }

    try:
        r = requests.get(url, params=params)
        return r.json()
    except:
        return []


def check_setup(symbol):

    global signals_today

    data = get_klines(symbol)

    if len(data) < 20:
        return

    c1, c2, c3 = data[-3], data[-2], data[-1]

    o1, cl1 = float(c1[1]), float(c1[4])
    o2, cl2 = float(c2[1]), float(c2[4])
    o3, cl3 = float(c3[1]), float(c3[4])

    body1 = abs(cl1 - o1)
    body2 = abs(cl2 - o2)
    body3 = abs(cl3 - o3)

    avg_body = sum(abs(float(x[4]) - float(x[1])) for x in data) / len(data)

    print(symbol, "scanned")

    if (
        body1 > avg_body * 1.2 and
        body3 > avg_body * 1.2 and
        body2 < body1 and
        body2 < body3 and
        body2 > avg_body * 0.1
    ):

        entry = cl3

        if cl3 > o3:
            direction = "BUY"
            tp = entry * (1 + TP_PERCENT / 100)
            sl = entry * (1 - SL_PERCENT / 100)
        else:
            direction = "SELL"
            tp = entry * (1 - TP_PERCENT / 100)
            sl = entry * (1 + SL_PERCENT / 100)

        active_trades[symbol] = {
            "direction": direction,
            "entry": entry,
            "tp": tp,
            "sl": sl
        }

        signals_today += 1

        print(symbol, "PATTERN FOUND")

        send_message(f"""🚀 TEST SIGNAL

Symbol: {symbol}
Type: {direction}
Timeframe: 5m

Entry: {entry:.8f}
TP: {tp:.8f}
SL: {sl:.8f}
""")


def check_results():

    global wins, losses

    for symbol in list(active_trades.keys()):

        try:

            price = float(requests.get(
                "https://api.binance.com/api/v3/ticker/price",
                params={"symbol": symbol}
            ).json()["price"])

        except:
            continue

        trade = active_trades[symbol]

        if trade["direction"] == "BUY":

            if price >= trade["tp"]:

                wins += 1

                send_message(f"""✅ TP HIT

Symbol: {symbol}

Wins: {wins}
Losses: {losses}
""")

                del active_trades[symbol]

            elif price <= trade["sl"]:

                losses += 1

                send_message(f"""❌ SL HIT

Symbol: {symbol}

Wins: {wins}
Losses: {losses}
""")

                del active_trades[symbol]

        else:

            if price <= trade["tp"]:

                wins += 1

                send_message(f"""✅ TP HIT

Symbol: {symbol}

Wins: {wins}
Losses: {losses}
""")

                del active_trades[symbol]

            elif price >= trade["sl"]:

                losses += 1

                send_message(f"""❌ SL HIT

Symbol: {symbol}

Wins: {wins}
Losses: {losses}
""")

                del active_trades[symbol]


def send_daily_report():

    global wins, losses, signals_today

    total = wins + losses

    if total > 0:
        winrate = (wins / total) * 100
    else:
        winrate = 0

    profit = (wins * 0.25) - (losses * 0.15)

    send_message(f"""📊 DAILY REPORT (24H)

Signals: {signals_today}
Wins: {wins}
Losses: {losses}

Winrate: {winrate:.2f} %

Estimated Profit: {profit:.2f} %

#BotPerformance
""")


print("🔥 BOT STARTED (TEST MODE)")


while True:

    for symbol in symbols:

        check_setup(symbol)

    check_results()

    now = datetime.datetime.now()

    if (now - start_time).total_seconds() >= 86400:

        send_daily_report()

        wins = 0
        losses = 0
        signals_today = 0

        start_time = datetime.datetime.now()

    time.sleep(150)
