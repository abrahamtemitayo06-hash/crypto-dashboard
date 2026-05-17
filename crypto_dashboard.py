import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ================== CONFIG ==================
st.set_page_config(page_title="Temitayo Crypto", layout="wide", page_icon="🪙")

coins = {
    "Bitcoin": "bitcoin", "Ethereum": "ethereum", "Solana": "solana",
    "Binance Coin": "binancecoin", "Cardano": "cardano", "Ripple": "ripple"
}

# ================== SIDEBAR ==================
st.sidebar.title("🪙 Crypto Selector")
selected_coin_name = st.sidebar.selectbox("Choose Cryptocurrency", options=list(coins.keys()))
selected_coin_id = coins[selected_coin_name]

# ================== MAIN TITLE ==================
st.title(f"✨ Temitayo's Professional Crypto Dashboard")
st.markdown(f"### Real-time tracking for **{selected_coin_name}**")

# ================== PRICE FETCH ==================
@st.cache_data(ttl=60)
def get_crypto_price(coin_id):
    try:
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd", 
            timeout=10
        )
        return res.json()[coin_id]["usd"]
    except:
        st.error("Could not fetch price. Please refresh.")
        return 0

crypto_price = get_crypto_price(selected_coin_id)

# ================== BEAUTIFUL PRICE CARD ==================
st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e1e1e, #0f0f0f); 
                padding: 40px; border-radius: 25px; text-align: center; 
                border: 3px solid #00ff88; box-shadow: 0 10px 30px rgba(0, 255, 136, 0.15);'>
        <h2 style='color: #aaaaaa; margin: 0 0 10px 0;'>Current {selected_coin_name} Price</h2>
        <h1 style='color: #00ff88; margin: 0; font-size: 4.2rem;'>${crypto_price:,.2f}</h1>
        <p style='color: #00ff88; font-size: 1.1rem;'>United States Dollar</p>
    </div>
""", unsafe_allow_html=True)

if st.button("🔄 Refresh All Data", type="primary"):
    st.rerun()

# ================== ALERT & TELEGRAM ==================
st.header("🚨 Price Alert System")

col1, col2 = st.columns([3, 1])
with col1:
    alert_price = st.number_input(f"Target Price for {selected_coin_name} (USD)", 
                                 min_value=1, value=int(crypto_price * 1.08), step=100)

with col2:
    if st.button("Check Alert", type="primary", use_container_width=True):
        if crypto_price >= alert_price:
            st.success(f"🎉 ALERT TRIGGERED! {selected_coin_name} is now above ${alert_price:,}!")
            st.balloons()
        else:
            st.info(f"Still below target of ${alert_price:,}")

# Telegram
st.subheader("📱 Telegram Notifications")
t1, t2 = st.columns(2)
with t1:
    telegram_token = st.text_input("Bot Token", type="password")
with t2:
    telegram_chat_id = st.text_input("Chat ID")

# ================== CHART & DOWNLOADS ==================
st.header(f"{selected_coin_name} 7-Day Price Trend")

try:
    history = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{selected_coin_id}/market_chart?vs_currency=usd&days=7",
        timeout=10
    )
    df = pd.DataFrame(history.json()["prices"], columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

    fig = px.line(df, x="date", y="price", 
                  title=f"{selected_coin_name} Price Movement",
                  template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # Download Buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📥 Download Chart as PNG", use_container_width=True):
            fig.write_image("chart.png")
            with open("chart.png", "rb") as f:
                st.download_button("Download PNG File", f, f"{selected_coin_name}_chart.png", "image/png")
    with c2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Price Data (CSV)", csv, f"{selected_coin_name}_data.csv", "text/csv")

except:
    st.error("Could not load chart. Please refresh.")

st.caption("Built with ❤️ by Temitayo • Lagos, Nigeria")