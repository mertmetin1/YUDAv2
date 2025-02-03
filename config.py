SYMBOL = "IBM"
SECTOR_SYMBOLS = ["AAPL", "GOOGL", "CSCO", "MSFT", "INTC"]
START_DATE = "2021-01-01"
END_DATE = None
#msft-ibm
weights = {
    "profitability": 0.25,
    "liquidity": 0.20,
    "risk": 0.15,
    "return": 0.25,
    "valuation": 0.10,
    "cash_flow": 0.05
}

dynamic_metrics = {
    "netMargin": {"category": "profitability"},
    "operatingMargin": {"category": "profitability"},
    "grossProfitMargin": {"category": "profitability"},
    "quickRatio": {"category": "liquidity"},
    "debtToEquity": {"category": "risk"},
    "interestCoverageRatio": {"category": "risk"},
    "roic": {"category": "return"},
    "cashConversionCycle": {"category": "cash_flow"},
    "PERatio": {"category": "valuation"},
    "PB_Ratio": {"category": "valuation"},
    "DividendYield": {"category": "valuation"},
    "ReturnOnAssets": {"category": "profitability"},  # Yeni metrik
    "ReturnOnEquity": {"category": "profitability"}   # Yeni metrik
}
