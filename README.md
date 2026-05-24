# Stock Signal Screener

A live stock screening tool that uses RSI and Moving Average crossover strategies to generate BUY/SELL/HOLD signals for any stock.

## Features
- Enter any stock ticker and get real-time signals
- RSI indicator with overbought/oversold detection
- 20-day and 50-day Moving Average crossover analysis
- Market screener for top 10 stocks (AAPL, TSLA, NVDA, META and more)
- Live price charts

## Tech Stack
- Python, Pandas, yfinance, Streamlit

## Live Demo
https://trading-screener-ivkgkv944he7cwey7kb6wy.streamlit.app

## How it works
- RSI < 30 + MA20 > MA50 = BUY signal
- RSI > 70 + MA20 < MA50 = SELL signal
- Everything else = HOLD
