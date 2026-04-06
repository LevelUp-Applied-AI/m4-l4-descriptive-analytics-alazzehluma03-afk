"""
Automated EDA Report Generator

Reusable module that generates an exploratory data analysis (EDA)
report for any pandas DataFrame.

Outputs:
- Data profile
- Distribution plots
- Correlation heatmap
- Missing data visualization
- Outlier summary (IQR method)
"""

import os
from matplotlib import style
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


# =====================================================
# 1. DATA PROFILE
# =====================================================

def data_profile(df, output_dir="output"):
    """Generate basic dataset profile."""

    shape = df.shape
    data_types = df.dtypes
    missing = df.isnull().sum()
    desc = df.describe()

    with open(f"{output_dir}/data_profile.txt", "w") as f:
        f.write("DATA PROFILE\n\n")

        f.write(f"Shape: {shape}\n\n")

        f.write("Data Types:\n")
        f.write(str(data_types))
        f.write("\n\n")

        f.write("Missing Values:\n")
        f.write(str(missing))
        f.write("\n\n")

        f.write("Descriptive Statistics:\n")
        f.write(str(desc))


# =====================================================
# 2. DISTRIBUTION PLOTS
# =====================================================

def plot_distributions(df, output_dir="output"):
    """Create distribution plots for all numeric columns."""

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        plt.figure()
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{col}_distribution.png")
        plt.close()


# =====================================================
# 3. CORRELATION ANALYSIS
# =====================================================

def plot_correlations(df, output_dir="output"):
    """Generate correlation heatmap."""

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        return  # nothing to correlate

    corr = numeric_df.corr(method="pearson")

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png")
    plt.close()


# =====================================================
# 4. MISSING DATA VISUALIZATION
# =====================================================

def plot_missing(df, output_dir="output"):
    """Visualize missing data pattern."""

    plt.figure(figsize=(10, 4))
    sns.heatmap(df.isnull(), cbar=False)
    plt.title("Missing Data Pattern")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/missing_values.png")
    plt.close()


# =====================================================
# 5. OUTLIER SUMMARY (IQR METHOD)
# =====================================================

def outlier_summary(df, output_dir="output"):
    """Detect outliers using IQR rule."""

    numeric_cols = df.select_dtypes(include=np.number).columns
    report = []

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        report.append(f"{col}: {outliers} outliers")

    with open(f"{output_dir}/outlier_summary.txt", "w") as f:
        f.write("\n".join(report))


# =====================================================
# 6. MAIN REPORT PIPELINE
# =====================================================

def generate_eda_report(
    df,
    output_dir="output",
    columns=None,
    style="darkgrid"
):
    """
    Run full automated EDA pipeline.

    Parameters:
        df : pandas DataFrame
        output_dir : directory to save results
    """

    os.makedirs(output_dir, exist_ok=True)

    sns.set_style(style)

    if columns is not None:
        df = df[columns]

    data_profile(df, output_dir)
    plot_distributions(df, output_dir)
    plot_correlations(df, output_dir)
    plot_missing(df, output_dir)
    outlier_summary(df, output_dir)

    print(f"EDA report generated in '{output_dir}/'")