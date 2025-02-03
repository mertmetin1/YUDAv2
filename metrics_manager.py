import pandas as pd
import numpy as np


class MetricsManager:
    def __init__(self, dynamic_metrics):
        self.metrics = dynamic_metrics

    def add_metric(self, name, category):
        self.metrics[name] = {"category": category}

    def remove_metric(self, name):
        self.metrics.pop(name, None)



    def scale_yuda_score(self, score):
        """
        Scale the YUDA score into qualitative categories.
        
        Args:
            score (float): The YUDA score.

        Returns:
            str: A qualitative category for the score.
        """
        if score >= 1.5:
            return "Very Attractive"
        elif score >= 0.5:
            return "Attractive"
        elif score >= -0.5:
            return "Neutral"
        elif score >= -1.5:
            return "Unattractive"
        else:
            return "Very Unattractive"

    def clean_and_calculate_metrics(self, income_df, balance_df, cashflow_df,info):
        income_df["netMargin"] = income_df.get("Net Income", 0) / income_df.get("Total Revenue", 1)
        income_df["operatingMargin"] = income_df.get("Operating Income", 0) / income_df.get("Total Revenue", 1)
        income_df["grossProfitMargin"] = income_df.get("Gross Profit", 0) / income_df.get("Total Revenue", 1)
        
        
        
        
            # Yeni metriklerin eklenmesi
        income_df["ReturnOnAssets"] = info.get("returnOnAssets", np.nan)
        income_df["ReturnOnEquity"] = info.get("returnOnEquity", np.nan)
            
            
        
        #yeni eklendi
        
        income_df["interestCoverageRatio"] = (
                        income_df.get("Operating Income", 0) /
                        (income_df.get("Interest Expense", 1) + 1e-9)
                    )
        balance_df["Invested Capital"] = (
            balance_df.get("Total Assets", 0) - balance_df.get("Current Liabilities", 0)
        )
        income_df["roic"] = (
            income_df.get("Net Income", 0) /
            (balance_df.get("Invested Capital", 1) + 1e-9)
        )

        income_df["PERatio"] = info.get("trailingPE", np.nan)
        income_df["PB_Ratio"] = info.get("priceToBook", np.nan)
        income_df["DividendYield"] = info.get("dividendYield", np.nan)








        balance_df["quickRatio"] = (
            (balance_df.get("Current Assets", 0) - balance_df.get("Inventory", 0)) /
            balance_df.get("Current Liabilities", 1)
        )
        balance_df["debtToEquity"] = (
            balance_df.get("Total Liabilities", 0) / balance_df.get("Common Stock Equity", 1)
        )

        cashflow_df["cashConversionCycle"] = (
            income_df.get("Accounts Receivable", 0) / income_df.get("Total Revenue", 1) +
            balance_df.get("Inventory", 0) / income_df.get("Total Revenue", 1) -
            balance_df.get("Accounts Payable", 0) / income_df.get("Total Revenue", 1)
        )

        combined_df = pd.merge(income_df, balance_df, left_index=True, right_index=True, how="outer")
        combined_df = pd.merge(combined_df, cashflow_df, left_index=True, right_index=True, how="outer")
        combined_df.dropna(thresh=3, inplace=True)




        return combined_df

    def calculate_z_scores(self, df):
        """
        Calculate z-scores for all metrics in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing metrics.

        Returns:
            pd.DataFrame: DataFrame with z-scores added for each metric.
        """
        for metric in self.metrics.keys():
            if metric in df.columns:
                df[f"{metric}_z"] = self.zscore(df[metric])
            else:
                print(f"Metric '{metric}' is missing in DataFrame.")
        return df
    def calculate_yuda_scores(self, df, weights, sector_means=None):
        """
        Calculate YUDA scores for the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing metrics and z-scores.
            weights (dict): A dictionary of category weights.
            sector_means (pd.Series): Sector averages for metrics (optional).

        Returns:
            pd.DataFrame: DataFrame with YUDA scores and categories.
        """
        df["enhanced_yuda_score"] = df.apply(
            lambda row: self.calculate_enhanced_yuda_score_dynamic(row, weights, sector_means), axis=1
        )
        df["yuda_score_category"] = df["enhanced_yuda_score"].apply(self.scale_yuda_score)
        return df


    def zscore(self, series):
        return (series - series.mean()) / (series.std() + 1e-9)

    def calculate_enhanced_yuda_score_dynamic(self, row, weights, sector_means=None):
        """
        Calculate Enhanced YUDA score dynamically, incorporating sector influence.

        Args:
            row (pd.Series): A row from the DataFrame.
            weights (dict): A dictionary of weights for each category.
            sector_means (pd.Series): Sector averages for metrics (optional).

        Returns:
            float: Calculated YUDA score.
        """
        score = 0
        for metric, config in self.metrics.items():
            z_col = f"{metric}_z"
            if z_col in row:
                metric_score = row[z_col]
                category_weight = weights.get(config["category"], 0)

                # Apply sector influence if available
                if sector_means is not None and metric in sector_means:
                    sector_mean = sector_means[metric]
                    sector_influence = (row[metric] - sector_mean) / (sector_mean + 1e-9)
                    metric_score += sector_influence

                score += metric_score * category_weight
        return score
