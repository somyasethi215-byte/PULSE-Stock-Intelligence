import time
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from model import predict_stock_price

st.set_page_config(
    page_title="Pulse | Stock Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Modern visual system + subtle motion ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #080b12;
        --panel: rgba(18, 24, 38, .78);
        --line: rgba(160, 180, 220, .14);
        --text: #eef3ff;
        --muted: #8c9ab4;
        --accent: #9bffb0;
        --accent2: #83b8ff;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(49, 112, 101, .20), transparent 34%),
            radial-gradient(ellipse at 88% 8%, rgba(75, 101, 184, .20), transparent 32%),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] { background: rgba(8, 11, 18, .70); }
    [data-testid="stSidebar"] {
        background: rgba(12, 17, 28, .95);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: var(--text); }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    .brand {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: .18em;
        text-transform: uppercase;
        color: var(--accent);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.3rem 2.4rem;
        border: 1px solid rgba(155, 255, 176, .20);
        border-radius: 28px;
        background: linear-gradient(120deg, rgba(22, 39, 47, .92), rgba(20, 26, 44, .88) 58%, rgba(31, 36, 62, .85));
        box-shadow: 0 18px 70px rgba(0,0,0,.22);
        animation: riseIn .7s ease-out both;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        right: -90px;
        top: -190px;
        border-radius: 50%;
        border: 1px solid rgba(155,255,176,.18);
        box-shadow: 0 0 0 32px rgba(155,255,176,.025), 0 0 0 66px rgba(155,255,176,.02);
        animation: orbitGlow 9s ease-in-out infinite alternate;
        pointer-events: none;
    }

    .eyebrow {
        color: var(--accent);
        font-size: .75rem;
        letter-spacing: .18em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: .8rem;
    }

    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        color: #f5f7ff;
        font-size: clamp(2.1rem, 4.6vw, 4rem);
        line-height: 1.02;
        letter-spacing: -.055em;
        margin: 0;
    }

    .hero h1 span {
        color: var(--accent);
        text-shadow: 0 0 32px rgba(155,255,176,.16);
    }

    .hero p {
        color: #aebbd0;
        max-width: 650px;
        font-size: 1rem;
        line-height: 1.7;
        margin-top: 1.1rem;
        margin-bottom: 0;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: .55rem;
        margin-top: 1.4rem;
        padding: .5rem .8rem;
        border: 1px solid rgba(155,255,176,.20);
        border-radius: 999px;
        color: #d9ffe0;
        background: rgba(155,255,176,.07);
        font-size: .8rem;
    }

    .pulse-dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 12px var(--accent);
        animation: pulseDot 1.7s infinite;
    }

    .section-head {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.45rem;
        font-weight: 600;
        letter-spacing: -.035em;
        margin: 1.8rem 0 .25rem;
    }

    .section-sub {
        color: var(--muted);
        font-size: .9rem;
        margin-bottom: 1.1rem;
    }

    .stock-card {
        padding: 1rem 1.05rem;
        min-height: 126px;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(23,31,47,.90), rgba(14,19,31,.92));
        transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
        animation: riseIn .55s ease both;
    }

    .stock-card:hover {
        transform: translateY(-5px);
        border-color: rgba(155,255,176,.45);
        box-shadow: 0 12px 32px rgba(0,0,0,.20);
    }

    .stock-card .company { color: #9aa9c3; font-size: .78rem; }
    .stock-card .ticker {
        font-family: 'Space Grotesk', sans-serif;
        color: #f3f6ff;
        font-size: 1.28rem;
        font-weight: 700;
        margin-top: .3rem;
    }
    .stock-card .tag {
        display: inline-block;
        margin-top: .65rem;
        padding: .25rem .55rem;
        border-radius: 8px;
        color: var(--accent);
        background: rgba(155,255,176,.08);
        font-size: .72rem;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(22,30,46,.92), rgba(14,19,31,.92));
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1rem 1.15rem;
        transition: transform .2s ease, border-color .2s ease;
        animation: riseIn .45s ease both;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(131,184,255,.35);
    }
    div[data-testid="stMetricLabel"] { color: #98a7c0 !important; }
    div[data-testid="stMetricValue"] { color: #f4f7ff !important; font-family: 'Space Grotesk', sans-serif; }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(155,255,176,.30);
        background: linear-gradient(100deg, #a3ffb5, #8de9cb);
        color: #07110d;
        font-weight: 700;
        min-height: 2.8rem;
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(155,255,176,.15);
        border-color: #b9ffca;
        color: #07110d;
    }

    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background: #111827;
        border-color: rgba(160,180,220,.20);
        border-radius: 12px;
    }

    .note {
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        background: rgba(15,21,34,.72);
        color: #aab7cc;
        font-size: .87rem;
        line-height: 1.6;
    }

    .footer {
        color: #697891;
        font-size: .78rem;
        text-align: center;
        padding-top: 1.5rem;
        letter-spacing: .02em;
    }

    @keyframes riseIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: .45; transform: scale(.78); }
    }
    @keyframes orbitGlow {
        from { transform: translate(0,0) rotate(0deg); }
        to { transform: translate(-18px, 18px) rotate(18deg); }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: .01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: .01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Stock list ----------
STOCKS = {
    "Apple": ("AAPL", "US"),
    "Microsoft": ("MSFT", "US"),
    "NVIDIA": ("NVDA", "US"),
    "Alphabet (Google)": ("GOOGL", "US"),
    "Amazon": ("AMZN", "US"),
    "Tesla": ("TSLA", "US"),
    "Reliance Industries": ("RELIANCE.NS", "India"),
    "Tata Consultancy Services": ("TCS.NS", "India"),
    "Infosys": ("INFY.NS", "India"),
    "HDFC Bank": ("HDFCBANK.NS", "India"),
    "ICICI Bank": ("ICICIBANK.NS", "India"),
    "State Bank of India": ("SBIN.NS", "India"),
}

# ---------- Sidebar ----------
st.sidebar.markdown('<div class="brand">✦ PULSE</div>', unsafe_allow_html=True)
st.sidebar.caption("Stock intelligence dashboard")
st.sidebar.divider()

market_filter = st.sidebar.radio("Market", ["All markets", "India", "US"], horizontal=False)
available_companies = [
    name for name, (_, market) in STOCKS.items()
    if market_filter == "All markets" or market == market_filter
]
selected_company = st.sidebar.selectbox("Choose a company", available_companies)
symbol = STOCKS[selected_company][0]
period = st.sidebar.selectbox("History range", ["6mo", "1y", "2y", "5y"], index=2)
st.sidebar.caption(f"Ticker: `{symbol}`")
analyze_button = st.sidebar.button("Analyze selected stock  ↗", type="primary", use_container_width=True)

st.sidebar.divider()
st.sidebar.caption("Market data is fetched when you run an analysis. No live recommendation is implied.")

# ---------- Hero ----------
st.markdown('<div class="brand">✦ PULSE / MARKET LAB</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">A clearer view of the market</div>
      <h1>Make data feel<br><span>less complicated.</span></h1>
      <p>Explore historical prices, compare a simple machine-learning estimate, and understand model error in one clean workspace.</p>
      <div class="status-pill"><span class="pulse-dot"></span> Analytics workspace · Ready to explore</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-head">Explore popular stocks</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Pick a company from the sidebar, then run an analysis. These are shortcuts, not investment recommendations.</div>', unsafe_allow_html=True)

popular = [
    ("Apple", "AAPL", "US market"),
    ("NVIDIA", "NVDA", "Semiconductors"),
    ("Microsoft", "MSFT", "Technology"),
    ("Reliance", "RELIANCE.NS", "Indian market"),
]
cols = st.columns(4)
for col, (company, ticker, tag) in zip(cols, popular):
    with col:
        st.markdown(
            f'<div class="stock-card"><div class="company">{company}</div>'
            f'<div class="ticker">{ticker}</div><div class="tag">{tag}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-head">Your analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Choose a stock on the left and press Analyze selected stock.</div>', unsafe_allow_html=True)

if analyze_button:
    try:
        with st.spinner("Connecting to market data and training the model…"):
            result = predict_stock_price(symbol=symbol, period=period)

        st.success(f"Analysis ready for {selected_company} ({result['symbol']}).")
        a, b, c = st.columns(3)
        a.metric("Latest close", f"{result['latest_close']:.2f}")
        b.metric("Model estimate · next session", f"{result['predicted_price']:.2f}")
        c.metric("Mean absolute error", f"{result['mae']:.2f}")

        st.caption("Currency is provided by the data source and may differ by market.")
        st.markdown('<div class="section-head">Price history</div>', unsafe_allow_html=True)
        history = result["history"]
        fig, ax = plt.subplots(figsize=(12, 4.8))
        fig.patch.set_alpha(0)
        ax.set_facecolor("#0d1320")
        ax.plot(history.index, history["Close"], linewidth=2, label="Closing price")
        ax.set_title(f"{result['symbol']} · Historical closing price", color="#edf3ff", pad=14)
        ax.set_xlabel("Date", color="#8c9ab4")
        ax.set_ylabel("Price", color="#8c9ab4")
        ax.tick_params(colors="#8c9ab4")
        for spine in ax.spines.values():
            spine.set_color("#293349")
        ax.grid(True, alpha=.15)
        ax.legend(facecolor="#111827", edgecolor="#293349", labelcolor="#edf3ff")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown('<div class="section-head">Actual vs model estimate</div>', unsafe_allow_html=True)
        comparison = pd.DataFrame(
            {"Actual price": result["actual_prices"], "Predicted price": result["predicted_prices"]},
            index=result["dates"],
        )
        st.line_chart(comparison)

        st.markdown('<div class="section-head">Model performance</div>', unsafe_allow_html=True)
        x, y = st.columns(2)
        x.metric("MAE", f"{result['mae']:.2f}")
        y.metric("RMSE", f"{result['rmse']:.2f}")
        st.markdown(
            '<div class="note"><b>MAE</b> is the average absolute difference between the test prices and model estimates. '
            '<b>RMSE</b> gives larger mistakes more influence. Lower values can indicate smaller errors on this test set, '
            'but they do not guarantee future accuracy.</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-head">Recent observations</div>', unsafe_allow_html=True)
        st.dataframe(history.tail(10), use_container_width=True)
        st.download_button(
            "Download historical data · CSV",
            data=history.to_csv().encode("utf-8"),
            file_name=f"{result['symbol']}_historical_data.csv",
            mime="text/csv",
        )
    except Exception as exc:
        st.error(f"Could not analyze {symbol}: {exc}")
        st.info("Check your internet connection and ticker. Try AAPL or RELIANCE.NS first.")

st.markdown(
    '<div class="note" style="margin-top:1.8rem"><b>Important:</b> This is an educational machine-learning demo, not financial advice. '
    'The estimate is not guaranteed and the simple model does not account for news, company fundamentals, or wider market conditions.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="footer">PULSE · STOCK INTELLIGENCE · PYTHON / STREAMLIT / SCIKIT-LEARN</div>', unsafe_allow_html=True)
