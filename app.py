import yfinance as yf
import pandas as pd
import streamlit as st

st.title("Stock Signal Screener")
st.caption("RSI + Moving Average signals for any stock")

ticker = st.text_input("Enter stock ticker", "AAPL")

df = yf.download(ticker, period="6mo", interval="1d", progress=False)
df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

# RSI
delta = df["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df["RSI"] = 100 - (100 / (1 + rs))

# Moving Averages
df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()

# Signal
def get_signal(row):
    if row["RSI"] < 30 and row["MA20"] > row["MA50"]:
        return "BUY"
    elif row["RSI"] > 70 and row["MA20"] < row["MA50"]:
        return "SELL"
    else:
        return "HOLD"

df["Signal"] = df.apply(get_signal, axis=1)

# Current RSI
current_rsi = float(df["RSI"].dropna().iloc[-1])
st.metric("Current RSI", f"{current_rsi:.2f}", delta="Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral")

# Charts
st.subheader("Price + Moving Averages")
st.line_chart(df[["Close", "MA20", "MA50"]])

st.subheader("RSI")
st.line_chart(df["RSI"])

st.subheader("Recent Signals")
st.dataframe(df[["Close", "RSI", "MA20", "MA50", "Signal"]].tail(20))

# Screener
st.subheader("Market Screener — Top Stocks")
tickers = ["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "AMZN", "NFLX", "AMD", "UBER"]
screener_data = []

for t in tickers:
    try:
        d = yf.download(t, period="3mo", interval="1d", progress=False)
        d.columns = [col[0] if isinstance(col, tuple) else col for col in d.columns]
        delta = d["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        rs = gain.rolling(14).mean() / loss.rolling(14).mean()
        rsi = float((100 - (100 / (1 + rs))).dropna().iloc[-1])
        ma20 = float(d["Close"].rolling(20).mean().dropna().iloc[-1])
        ma50 = float(d["Close"].rolling(50).mean().dropna().iloc[-1])
        price = float(d["Close"].dropna().iloc[-1])
        if rsi < 30 and ma20 > ma50:
            signal = "🟢 BUY"
        elif rsi > 70 and ma20 < ma50:
            signal = "🔴 SELL"
        else:
            signal = "⚪ HOLD"
        screener_data.append({"Ticker": t, "Price": round(price, 2), "RSI": round(rsi, 2), "Signal": signal})
    except:
        pass

st.dataframe(pd.DataFrame(screener_data))