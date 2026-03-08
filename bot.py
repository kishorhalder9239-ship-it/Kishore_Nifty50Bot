import requests
import time

BOT_TOKEN = "8739303828:AAG9zPZmjEmKv5SEbA95rFHzvtZsHNiNLUo"
CHAT_ID = "1780972347"

symbols = [
"BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
"ADAUSDT","DOGEUSDT","AVAXUSDT","TRXUSDT","DOTUSDT"
]

# ---------- TELEGRAM ----------

def send_message(text):

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url,data={"chat_id":CHAT_ID,"text":text},timeout=10)
    except Exception as e:
        print("Telegram error:",e)


# ---------- BINANCE DATA ----------

def get_klines(symbol):

    url="https://api.binance.com/api/v3/klines"

    params={
        "symbol":symbol,
        "interval":"5m",
        "limit":100
    }

    try:
        r=requests.get(url,params=params,timeout=10)
        return r.json()
    except:
        return []


# ---------- EMA ----------

def calculate_ema(prices,period=50):

    k=2/(period+1)

    ema=prices[0]

    for price in prices:
        ema=price*k+ema*(1-k)

    return ema


# ---------- RSI ----------

def calculate_rsi(prices,period=14):

    gains=[]
    losses=[]

    for i in range(1,len(prices)):

        diff=prices[i]-prices[i-1]

        if diff>0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain=sum(gains[-period:])/period
    avg_loss=sum(losses[-period:])/period

    if avg_loss==0:
        return 100

    rs=avg_gain/avg_loss

    rsi=100-(100/(1+rs))

    return rsi


# ---------- SIGNAL LOGIC ----------

def check_signal(symbol):

    data=get_klines(symbol)

    if len(data)<60:
        return

    closes=[float(x[4]) for x in data]

    ema50=calculate_ema(closes)

    rsi=calculate_rsi(closes)

    last=data[-2]
    prev=data[-3]
    mother=data[-4]

    o1=float(prev[1])
    c1=float(prev[4])

    o2=float(last[1])
    c2=float(last[4])

    high_prev=float(prev[2])
    low_prev=float(prev[3])

    high_mother=float(mother[2])
    low_mother=float(mother[3])


    # ---------- BULLISH ENGULFING ----------

    if c1<o1 and c2>o2 and c2>o1 and o2<c1:

        if c2>ema50 and rsi>55:

            send_message(f"""
🚀 BUY SIGNAL

Symbol: {symbol}
Pattern: Bullish Engulfing
Price: {c2}
EMA50: {round(ema50,2)}
RSI: {round(rsi,2)}
""")


    # ---------- BEARISH ENGULFING ----------

    if c1>o1 and c2<o2 and c2<o1 and o2>c1:

        if c2<ema50 and rsi<45:

            send_message(f"""
🔻 SELL SIGNAL

Symbol: {symbol}
Pattern: Bearish Engulfing
Price: {c2}
EMA50: {round(ema50,2)}
RSI: {round(rsi,2)}
""")


    # ---------- INSIDE BAR ----------

    if high_prev < high_mother and low_prev > low_mother:

        # BUY breakout
        if c2>high_mother and c2>ema50 and rsi>55:

            send_message(f"""
🚀 BUY SIGNAL

Symbol: {symbol}
Pattern: Inside Bar Breakout
Price: {c2}
""")


        # SELL breakout
        if c2<low_mother and c2<ema50 and rsi<45:

            send_message(f"""
🔻 SELL SIGNAL

Symbol: {symbol}
Pattern: Inside Bar Breakout
Price: {c2}
""")


# ---------- MAIN LOOP ----------

print("BOT STARTED")


while True:

    try:

        for symbol in symbols:

            print("Scanning",symbol)

            check_signal(symbol)

            time.sleep(1)

        print("Waiting next scan")

        time.sleep(300)

    except Exception as e:

        print("Main loop error:",e)

        time.sleep(10)
