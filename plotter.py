import matplotlib.pyplot as plt


def plot_combined(weights, merged_df, historical_data,SYMBOL):
    """Plot YUDA scores and stock price."""
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), gridspec_kw={"width_ratios": [1, 2]})

    # Bar Chart for Weights
    categories = list(weights.keys())
    values = list(weights.values())
    axes[0].bar(categories, values, color="skyblue")
    for i, v in enumerate(values):
        axes[0].text(i, v + 0.01, f"{v * 100:.1f}%", ha="center", fontsize=10, color="black")
    axes[0].set_title("Metrics Categories and Weights")
    axes[0].set_ylabel("Weight")
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)

    # Scaled YUDA Score with Stock Price
    ax1 = axes[1]
    ax2 = ax1.twinx()

    colors = {
        "Very Attractive": "green",
        "Attractive": "lime",
        "Neutral": "yellow",
        "Unattractive": "orange",
        "Very Unattractive": "red"
    }
    categories = merged_df["yuda_score_category"].unique()

    for category in categories:
        category_data = merged_df[merged_df["yuda_score_category"] == category]
        ax1.scatter(category_data.index, category_data["enhanced_yuda_score"],
                    label=category, color=colors[category], alpha=0.7)

    ax1.axhline(1.5, color="green", linestyle="--", label="Very Attractive Threshold")
    ax1.axhline(0.5, color="lime", linestyle="--", label="Attractive Threshold")
    ax1.axhline(-0.5, color="orange", linestyle="--", label="Unattractive Threshold")
    ax1.axhline(-1.5, color="red", linestyle="--", label="Very Unattractive Threshold")
    ax1.set_title(f"{SYMBOL} - Scaled YUDA Score and Stock Price")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Enhanced YUDA Score")
    ax1.legend(loc="upper left")
    ax1.grid(True)

    # Plot Stock Price
    ax2.plot(historical_data.index, historical_data["Close"], color="blue", label="Stock Price", alpha=0.6)
    ax2.set_ylabel("Stock Price (USD)", color="blue")
    ax2.tick_params(axis='y', labelcolor="blue")

    # Combine Legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    axes[1].legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right")

    # Adjust layout
    plt.tight_layout()
    plt.show()
 