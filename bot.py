last = data.iloc[-1]
prev = data.iloc[-2]

body = abs(last['Close'] - last['Open'])
body1 = abs(prev['Close'] - prev['Open'])

if body > body1:
    direction = "BUY" if last['Close'] > last['Open'] else "SELL"

    entry = round(last['Close'], 4)
    tp = round(entry * 1.003, 4)
    sl = round(entry * 0.998, 4)

    message = f"""
🚀 BIGSMALLBIG ALERT

Symbol: {symbol}
Timeframe: 5m
Direction: {direction}
Entry: {entry}
TP: {tp}
SL: {sl}
"""

    send_message(message)
