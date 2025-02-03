from config import SYMBOL, SECTOR_SYMBOLS, START_DATE, END_DATE, weights, dynamic_metrics
from data_fetcher import fetch_sector_data, fetch_yfinance_data
from metrics_manager import MetricsManager
from plotter import plot_combined

# Initialize Metrics Manager
metrics_manager = MetricsManager(dynamic_metrics)



"""
# Add and remove metrics for testing
metrics_manager.add_metric("currentRatio", "liquidity")
print("\nAdded 'currentRatio' metric to dynamic metrics.")

metrics_manager.remove_metric("PB_Ratio")
print("\nRemoved 'PB_Ratio' metric from dynamic metrics.")

"""


# Fetch data for the target symbol
info, income_df, balance_df, cashflow_df, historical_data = fetch_yfinance_data(SYMBOL, START_DATE, END_DATE)

# Fetch Sector Data
sector_df, sector_means = fetch_sector_data(SECTOR_SYMBOLS, START_DATE, END_DATE)

# Clean and calculate metrics
income_df = metrics_manager.clean_and_calculate_metrics(income_df, balance_df, cashflow_df, info)

# Calculate Z-scores
income_df = metrics_manager.calculate_z_scores(income_df)

# Fetch Sector Data
sector_df, sector_means = fetch_sector_data(SECTOR_SYMBOLS, START_DATE, END_DATE)

# Calculate YUDA Scores
income_df = metrics_manager.calculate_yuda_scores(income_df, weights, sector_means)


# Debugging Output
print("Enhanced YUDA Scores and Categories:")
print(income_df[["enhanced_yuda_score", "yuda_score_category"]].head())

# Plot Combined Data
plot_combined(weights, income_df, historical_data,SYMBOL=SYMBOL)

# Display Results
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

print("\n===== Sector df =====")
print(sector_df)

print("\n===== Sector Averages =====")
print(sector_means)

print("\n===== Symbol Information =====")
print(f"Symbol: {SYMBOL}")
print(f"Company Name: {info.get('longName', 'N/A')}")
print(f"Industry: {info.get('industry', 'N/A')}")
print(f"Sector: {info.get('sector', 'N/A')}")
print(f"Country: {info.get('country', 'N/A')}")


