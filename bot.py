import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

TP_PERCENT = 0.25
SL_PERCENT = 0.15

symbols = [symbols = [
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

last_signal = {}
active_trades = {}

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
        "limit":120
    }

    try:
        return requests.get(url,params=params,timeout=10).json()
    except:
        return []


def build_candle(candles):

    o = float(candles[0][1])
    c = float(candles[-1][4])

    highs = [float(x[2]) for x in candles]
    lows  = [float(x[3]) for x in candles]

    h = max(highs)
    l = min(lows)

    return o,h,l,c


def check_pattern(symbol,data,tf_size,tf_name):

    if len(data) < tf_size*4:
        return

    c1 = build_candle(data[-tf_size*4:-tf_size*3])
    c2 = build_candle(data[-tf_size*3:-tf_size*2])
    c3 = build_candle(data[-tf_size*2:-tf_size])

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

        send_message(f"""
🚀 SIGNAL

Symbol: {symbol}
Type: {direction}
Timeframe: {tf_name}

Entry: {entry}
""")


def scan_symbol(symbol):

    data = get_klines(symbol)

    if not data:
        return

    # 5m
    check_pattern(symbol,data,1,"5m")

    # 15m
    check_pattern(symbol,data,3,"15m")

    # 30m
    check_pattern(symbol,data,6,"30m")

    # 1h
    check_pattern(symbol,data,12,"1h")


print("BOT STARTED")

while True:

    print("Scanning market")

    for symbol in symbols:

        scan_symbol(symbol)

        time.sleep(0.5)

    print("Waiting next scan")

    time.sleep(300)
