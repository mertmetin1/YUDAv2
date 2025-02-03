import yfinance as yf


def fetch_yfinance_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    info = stock.info
    financials = stock.financials.T
    balance_sheet = stock.balance_sheet.T
    cashflow = stock.cashflow.T
    historical_data = stock.history(start=start_date, end=end_date)
    return info, financials, balance_sheet, cashflow, historical_data



import pandas as pd
import numpy as np

import pandas as pd
import numpy as np
from data_fetcher import fetch_yfinance_data

def fetch_sector_data(sector_symbols, start_date, end_date):
    """
    Fetch sector data for the given symbols and calculate sector averages.

    Args:
        sector_symbols (list): A list of stock symbols for the sector.
        start_date (str): The start date for fetching historical data.
        end_date (str): The end date for fetching historical data.

    Returns:
        tuple: A tuple containing:
            - sector_df (pd.DataFrame): DataFrame with the fetched sector data.
            - sector_means (pd.Series): Mean values for numeric columns in the sector data.
    """
    records = []
    for sym in sector_symbols:
        # Fetch data for each symbol
        info, _, _, _, _ = fetch_yfinance_data(sym, start_date, end_date)
        
        # Append relevant metrics to records
        records.append({
            "symbol": sym,
            "PERatio": info.get("trailingPE", np.nan),
            "PB_Ratio": info.get("priceToBook", np.nan),
            "DividendYield": info.get("dividendYield", np.nan),
            "ReturnOnAssets": info.get("returnOnAssets", np.nan),
            "ReturnOnEquity": info.get("returnOnEquity", np.nan)
        })
    
    # Create DataFrame and calculate means
    sector_df = pd.DataFrame(records)
    sector_means = sector_df.mean(numeric_only=True)
    
    return sector_df, sector_means
