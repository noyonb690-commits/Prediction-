import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from model import train_model, predict
from storage import load_feedback, save_feedback

st.title("📊 AI Trading Dashboard (Live + Auto Learning)")

pair = st.text_input("Forex Pair", "EURUSD=X")

# Load data
data = yf.download(pair, period="60d", interval="1h")

# Load feedback memory
feedback = load_feedback()

# Train model
model = train_model(data, feedback)

# Prediction
pred, prob = predict(model, data)

# ---- LIVE CANDLE CHART ----
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
))

st.plotly_chart(fig)

# ---- AI SIGNAL ----
if pred == 1:
    st.success("📈 AI Signal: UP")
else:
    st.error("📉 AI Signal: DOWN")

st.write("Confidence:", prob)

# ---- YES / NO FEEDBACK ----
st.subheader("Did AI prediction match reality?")

col1, col2 = st.columns(2)

if col1.button("YES"):
    feedback.append({"result": "yes"})
    save_feedback(feedback)
    st.success("Saved YES feedback → model will improve")

if col2.button("NO"):
    feedback.append({"result": "no"})
    save_feedback(feedback)
    st.error("Saved NO feedback → model will adjust next time")

st.write("Total feedback stored:", len(feedback))
