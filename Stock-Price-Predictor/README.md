# PULSE — Stock Intelligence Dashboard

A modern Streamlit stock-analysis demo with a dark visual theme, animated hero treatment, hoverable stock cards, stock selection, historical charts, a simple Linear Regression estimate, model evaluation, and CSV export.

## Run on Windows / VS Code

1. Extract the ZIP and open the `Stock-Price-Predictor-Modern` folder in VS Code.
2. Open Terminal → New Terminal.
3. Activate your existing Python environment if it already has working dependencies. Otherwise, Python 3.12 is recommended:
   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
4. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Run:
   ```powershell
   python -m streamlit run app.py
   ```
6. Open `http://localhost:8501` if the browser does not launch automatically.

## Included files
- `app.py` — modern animated dashboard and UI
- `model.py` — stock data and Linear Regression model
- `requirements.txt` — dependencies

## Notes
- Internet access is required to retrieve market data.
- Example tickers include `AAPL`, `MSFT`, `NVDA`, `RELIANCE.NS`, and `TCS.NS`.
- The listed stocks are shortcuts only; they are not personalized or live investment recommendations.
- This is an educational demo, not financial advice. Model estimates are not guaranteed.
- The visual uses subtle CSS animations and may load Google Fonts from the internet; it still functions if the fonts fail to load.
