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

last_signal = {}
active_trades = {}

wins = 0
losses = 0


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except:
        pass


def get_klines(symbol):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "5m",
        "limit": 10
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except:
        return []


def check_setup(symbol):

    global last_signal

    data = get_klines(symbol)

    if len(data) < 5:
        return

    # last closed candles
    c1 = data[-3]
    c2 = data[-2]
    c3 = data[-1]

    o1, cl1 = float(c1[1]), float(c1[4])
    o2, cl2 = float(c2[1]), float(c2[4])
    o3, cl3 = float(c3[1]), float(c3[4])

    body1 = abs(cl1 - o1)
    body2 = abs(cl2 - o2)

    candle_time = c3[0]

    if symbol in last_signal and last_signal[symbol] == candle_time:
        return

    # BIG → SMALL → SAME DIRECTION

    if body2 < body1 * 0.4:

        if cl1 > o1 and cl3 > o3:
            direction = "BUY"

        elif cl1 < o1 and cl3 < o3:
            direction = "SELL"

        else:
            return

        last_signal[symbol] = candle_time

        entry = float(cl3)

        if direction == "BUY":
            tp = entry * (1 + TP_PERCENT / 100)
            sl = entry * (1 - SL_PERCENT / 100)

        else:
            tp = entry * (1 - TP_PERCENT / 100)
            sl = entry * (1 + SL_PERCENT / 100)

        active_trades[symbol] = {
            "direction": direction,
            "entry": entry,
            "tp": tp,
            "sl": sl
        }

        send_message(f"""
🚀 SIGNAL

Symbol: {symbol}
Type: {direction}
Timeframe: 5m

Entry: {entry}
TP: {tp}
SL: {sl}
""")


def check_results():

    global wins, losses

    for symbol in list(active_trades.keys()):

        try:

            price = float(
                requests.get(
                    "https://api.binance.com/api/v3/ticker/price",
                    params={"symbol": symbol},
                    timeout=10
                ).json()["price"]
            )

        except:
            continue

        trade = active_trades[symbol]

        if trade["direction"] == "BUY":

            if price >= trade["tp"]:

                wins += 1
                send_message(f"✅ TP HIT {symbol}\nWins: {wins}\nLosses: {losses}")
                del active_trades[symbol]

            elif price <= trade["sl"]:

                losses += 1
                send_message(f"❌ SL HIT {symbol}\nWins: {wins}\nLosses: {losses}")
                del active_trades[symbol]

        else:

            if price <= trade["tp"]:

                wins += 1
                send_message(f"✅ TP HIT {symbol}\nWins: {wins}\nLosses: {losses}")
                del active_trades[symbol]

            elif price >= trade["sl"]:

                losses += 1
                send_message(f"❌ SL HIT {symbol}\nWins: {wins}\nLosses: {losses}")
                del active_trades[symbol]


print("🔥 BOT STARTED")


while True:

    for symbol in symbols:

        check_setup(symbol)

        time.sleep(1)

    check_results()

    time.sleep(120)
