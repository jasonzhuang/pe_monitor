import yfinance as yf
import pandas as pd
import datetime
import yaml
from utils.push import send_email, send_wechat

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_pe_percentile(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5y", interval="1d")
        if 'Close' not in hist.columns:
            return None, None, None
        pe_ratio = stock.info.get("trailingPE")
        pe_history = [v for v in stock.history_metadata.get('trailingPE', []) if v]
        if not pe_ratio or not pe_history:
            return None, None, None
        pe_series = pd.Series(pe_history)
        percentile = (pe_series < pe_ratio).sum() / len(pe_series) * 100
        return pe_ratio, percentile, stock.info.get("shortName", ticker)
    except Exception as e:
        return None, None, ticker

def main():
    config = load_config()
    results = []
    for ticker in config['stocks']:
        pe, perc, name = get_pe_percentile(ticker)
        if pe is None:
            continue
        if perc < config['threshold_percentile']:
            results.append(f"{name}（{ticker}）：PE={pe:.2f}，分位={perc:.1f}%")

    if results:
        content = "\n".join(results)
        if config['email']['enable']:
            send_email("低估提醒", content, config['email'])
        if config['wechat']['enable']:
            send_wechat(content, config['wechat']['sckey'])

if __name__ == "__main__":
    main()