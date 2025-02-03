import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from config import SYMBOL, SECTOR_SYMBOLS, START_DATE, END_DATE, weights, dynamic_metrics
from data_fetcher import fetch_sector_data, fetch_yfinance_data
from metrics_manager import MetricsManager
from plotter import plot_combined

# Initialize Metrics Manager
metrics_manager = MetricsManager(dynamic_metrics)

# Veri çekim işlemleri
try:
    info, income_df, balance_df, cashflow_df, historical_data = fetch_yfinance_data(SYMBOL, START_DATE, END_DATE)
    sector_df, sector_means = fetch_sector_data(SECTOR_SYMBOLS, START_DATE, END_DATE)
except Exception as e:
    raise RuntimeError(f"Veri çekimi başarısız: {e}")

# Verilerin boş olup olmadığını kontrol edin
if historical_data.empty or income_df.empty:
    raise ValueError("Veriler çekilemedi veya boş. SYMBOL, START_DATE ve END_DATE değerlerini kontrol edin.")

# Metrik hesaplama ve YUDA skoru oluşturma
income_df = metrics_manager.clean_and_calculate_metrics(income_df, balance_df, cashflow_df, info)
income_df = metrics_manager.calculate_z_scores(income_df)
income_df = metrics_manager.calculate_yuda_scores(income_df, weights, sector_means)

# Backtesting için veri hazırlığı
if "Close" not in historical_data.columns:
    raise ValueError("Historical data 'Close' sütununu içermiyor.")
backtest_df = pd.merge(
    income_df[["enhanced_yuda_score", "yuda_score_category"]],
    historical_data[["Close"]],
    left_index=True,
    right_index=True,
    how="inner"
)

if backtest_df.empty:
    raise ValueError("Backtest için uygun veri oluşturulamadı. Lütfen verilerin zaman eksenlerini kontrol edin.")

# Başlangıç sermayesi ve pozisyon
initial_capital = 10000
capital = initial_capital
position = 0  # 1: Alım yapıldı, 0: Pozisyon yok
returns = []

# Backtesting stratejisi
for i in range(1, len(backtest_df)):
    score = backtest_df["enhanced_yuda_score"].iloc[i]
    price = backtest_df["Close"].iloc[i]

    if score >= 1.5 and position == 0:  # Alım yap
        buy_price = price
        position = capital / price
        capital = 0  # Tüm sermaye yatırıldı

    elif score <= -0.5 and position > 0:  # Satış yap
        sell_price = price
        capital = position * price
        position = 0
        returns.append((sell_price - buy_price) / buy_price)  # Getiri hesapla

# Kümülatif getiriyi hesapla
cumulative_return = np.prod([1 + r for r in returns]) - 1
print(f"Kümülatif Getiri: {cumulative_return * 100:.2f}%")

# Grafik oluşturma
plt.figure(figsize=(10, 6))
plt.plot(backtest_df.index, backtest_df["Close"], label="Stock Price")
plt.title("Backtesting: Hisse Fiyatı ve YUDA Skorları")
plt.xlabel("Tarih")
plt.ylabel("Fiyat")
plt.legend()
plt.grid()
plt.show()

# Sonuçları yazdırma
print("\n===== Latest YUDA Score =====")
latest_yuda_score = income_df["enhanced_yuda_score"].iloc[-1]
latest_category = metrics_manager.scale_yuda_score(latest_yuda_score)
print(f"Symbol: {SYMBOL}")
print(f"YUDA Score: {latest_yuda_score:.2f}")
print(f"Category: {latest_category}")

print("\n===== Metrics =====")
for metric in dynamic_metrics.keys():
    if metric in income_df:
        print(f"{metric}: {income_df[metric].iloc[-1]:.4f}")
    else:
        print(f"{metric}: Data not available")
