import yfinance as yf
import pandas as pd
import streamlit as st

st.title("Stock Signal Screener")
st.caption("RSI + Moving Average signals for any stock")

ticker = st.text_input("Enter stock ticker", "AAPL")

df = yf.download(ticker, period="6mo", interval="1d")

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

# Flatten columns
df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

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
current_rsi = df["RSI"].iloc[-1]
st.metric("Current RSI", f"{current_rsi:.2f}", delta="Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral")

# Price chart
st.subheader("Price + Moving Averages")
st.line_chart(df[["Close", "MA20", "MA50"]])

# RSI chart
st.subheader("RSI")
st.line_chart(df["RSI"])

# Signal table
st.subheader("Recent Signals")
st.dataframe(df[["Close", "RSI", "MA20", "MA50", "Signal"]].tail(20))
st.subheader("Market Screener — Top Stocks")

tickers = ["AAPL", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "AMZN", "NFLX", "AMD", "UBER"]

screener_data = []

for t in tickers:
    try:
        d = yf.download(t, period="3mo", interval="1d", progress=False)
        delta = d["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        rsi = (100 - (100 / (1 + rs))).iloc[-1].item()
        ma20 = d["Close"].rolling(20).mean().iloc[-1].item()
        ma50 = d["Close"].rolling(50).mean().iloc[-1].item()
        price = d["Close"].iloc[-1].item()
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