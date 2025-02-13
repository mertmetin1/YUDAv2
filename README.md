# YUDA Score - Advanced Financial Analysis and Stock Evaluation System

## Overview
YUDA Score is a sophisticated financial analysis tool designed to evaluate stocks based on a wide range of financial metrics, providing investors and analysts with deep insights into a stock's overall attractiveness. The system integrates real-time data retrieval, metric computations, benchmarking against sector averages, and visualization to support data-driven investment decisions.

## Key Features
### 📊 Real-time Financial Data Retrieval
- Utilizes Yahoo Finance API to fetch fundamental stock and sector-level data.
- Retrieves financial statements, balance sheets, and cash flow reports.

### 🔍 Dynamic Financial Metrics Calculation
- Computes key financial indicators across various categories:
  - **Profitability**: Net Margin, Operating Margin, Return on Assets (ROA), Return on Equity (ROE).
  - **Liquidity**: Quick Ratio, Current Ratio.
  - **Risk Assessment**: Debt-to-Equity Ratio, Interest Coverage Ratio.
  - **Valuation**: Price-to-Earnings (P/E) Ratio, Price-to-Book (P/B) Ratio, Dividend Yield.
  - **Cash Flow Analysis**: Cash Conversion Cycle, Free Cash Flow.

### 📈 Sector-Based Benchmarking
- Compares a stock's financial metrics with its sector peers.
- Computes sector averages and integrates them into scoring.

### 🔬 Z-Score Standardization & Outlier Detection
- Normalizes financial data to ensure comparability across different industries and market conditions.
- Detects and adjusts for extreme outliers.

### 🎯 Enhanced YUDA Score Calculation
- Generates a **comprehensive stock attractiveness score** by weighting financial categories.
- Categorizes stocks as:
  - ✅ **Very Attractive** (≥ 1.5)
  - 👍 **Attractive** (0.5 to 1.5)
  - 😐 **Neutral** (-0.5 to 0.5)
  - ❌ **Unattractive** (-1.5 to -0.5)
  - 🚨 **Very Unattractive** (< -1.5)

### 📊 Data Visualization & Reporting
- **Bar Charts** for financial metric weights.
- **Time-Series Stock Price vs. YUDA Score Trends**.
- **Sector Comparisons & Score Distributions**.
- **Interactive visualizations** powered by Matplotlib.

## Technical Architecture
```
├── data_fetcher.py          # Retrieves stock & sector financial data
├── metrics_manager.py       # Computes and normalizes financial metrics
├── sector_manager.py        # Manages stock sector comparisons
├── weights_manager.py       # Handles dynamic weighting for financial categories
├── plotter.py               # Generates financial data visualizations
├── config.py                # Configuration settings (symbols, weights, metrics)
├── app.py                   # Main script to execute the YUDA Score pipeline
├── requirements.txt         # Dependencies list
└── README.md                # Documentation
```

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/mertmetin1/yuda-score.git
   cd yuda-score
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide
To compute financial scores and visualize insights, run:
```bash
python app.py
```
### Expected Outputs:
- **Financial Metric Reports** 📑
- **Sector Comparisons & Benchmarking** 📊
- **YUDA Score Calculations & Rankings** 🎯
- **Stock Valuation Trends & Graphs** 📉

## How YUDA Score Works
1. **Data Collection**: Fetches stock and sector financials.
2. **Metric Normalization**: Applies Z-score transformations.
3. **Sector Comparisons**: Evaluates company performance against industry norms.
4. **Score Computation**: Weighs different financial factors based on category importance.
5. **Visualization**: Displays results with plots and tables.

## Example Calculation
Using the following **customizable weight configuration**:
```python
weights = {
    "profitability": 0.25,
    "liquidity": 0.20,
    "risk": 0.15,
    "return": 0.25,
    "valuation": 0.10,
    "cash_flow": 0.05
}
```
Each stock is scored based on:
```
YUDA Score = Σ (Z-Score of Financial Metric * Category Weight)
```
Higher scores indicate **stronger financial health & investment potential**.

## Data Visualization
![resim](https://github.com/user-attachments/assets/dc1d2ac7-0df4-4c99-81c7-c1b18196208c)



## Customization & Extensibility
- **Modify Weights**: Adjust importance of each financial category in `config.py`.
- **Add New Metrics**: Extend `metrics_manager.py` to include additional financial indicators.
- **Change Sector Comparisons**: Edit stock sector configurations in `sector_manager.py`.
- **Enhance Visualizations**: Customize charting options in `plotter.py`.


🔥 **Enhance your stock analysis with YUDA Score today!** 🚀

