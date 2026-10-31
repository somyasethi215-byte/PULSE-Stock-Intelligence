import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


def predict_stock_price(symbol="AAPL", period="2y"):
    """Download historical data and train a basic linear regression model."""
    raw = yf.Ticker(symbol).history(period=period, auto_adjust=True)

    if raw.empty or "Close" not in raw.columns:
        raise ValueError("No usable stock data returned. Check the ticker and internet connection.")

    history = raw[["Close"]].dropna().copy()
    if len(history) < 50:
        raise ValueError("Not enough historical data. Choose a longer period or another ticker.")

    data = history.copy()
    for lag in range(1, 6):
        data[f"Previous_{lag}"] = data["Close"].shift(lag)
    data = data.dropna()

    features = [f"Previous_{lag}" for lag in range(1, 6)]
    X, y = data[features], data["Close"]

    split = int(len(data) * 0.8)
    if split <= 0 or split >= len(data):
        raise ValueError("Not enough data to create training and testing sets.")

    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = LinearRegression()
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)

    latest = history["Close"].iloc[-5:].to_numpy()[::-1]
    next_features = pd.DataFrame([latest], columns=features)
    next_price = float(model.predict(next_features)[0])

    return {
        "symbol": symbol.upper(),
        "latest_close": float(history["Close"].iloc[-1]),
        "predicted_price": next_price,
        "mae": float(mean_absolute_error(y_test, predicted)),
        "rmse": float(mean_squared_error(y_test, predicted) ** 0.5),
        "dates": y_test.index,
        "actual_prices": y_test.to_numpy(),
        "predicted_prices": predicted,
        "history": history,
    }
