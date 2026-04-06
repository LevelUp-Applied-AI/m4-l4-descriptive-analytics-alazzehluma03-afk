"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
from seaborn.objects import KDE
from torch import Use
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def load_and_profile(filepath):
    """Load the dataset and generate a data profile report.

    Args:
        filepath: path to the CSV file (e.g., 'data/student_performance.csv')

    Returns:
        DataFrame: the loaded dataset

    Side effects:
        Saves a text profile to output/data_profile.txt containing:
        - Shape (rows, columns)
        - Data types for each column
        - Missing value counts per column
        - Descriptive statistics for numeric columns
    """
    # TODO: Load the dataset and report its shape, data types, missing values,
    #       and descriptive statistics to output/data_profile.txt
    
    df = pd.read_csv(filepath)
    with open("output/data_profile.txt", "w") as f:
        f.write(f"Shape: {df.shape}\n\n")
        f.write("Data Types:\n")
        f.write(f"{df.dtypes}\n\n")
        f.write("Missing Values:\n")
        f.write(f"{df.isnull().sum()}\n\n")
        f.write("Descriptive Statistics:\n")
        f.write(f"{df.describe()}\n")
        return df
    
def clean_data(df):
    """Perform data cleaning and preprocessing.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        pandas DataFrame: the cleaned dataset
    """
    # TODO: Implement data cleaning steps (e.g., handling missing values, removing duplicates)
    df = df.copy()
    # Example: Fill missing numeric values with the median
    df['commute_minutes'] = df['commute_minutes'].fillna(
        df['commute_minutes'].median()
    )    
    df = df.dropna(subset=["study_hours_weekly"])
    return df
    #Justification for cleaning steps:
    #- Filling missing commute_minutes with the median is appropriate because it is a numeric variable that may have outliers, and the median is less sensitive to outliers than the mean.
    # dropping the rows with missing study_hours_weekly (~5%, roughly MCAR) is suitable and justifiable.
    #Why it's okay:
    #MCAR → No bias introduced by dropping.
    #Only 5% data loss → Minimal impact on sample size and power.
    #Keeps the dataset clean and simple (no imputation needed)

def plot_distributions(df):
    """Create distribution plots for key numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least 3 distribution plots (histograms with KDE or box plots)
        as PNG files in the output/ directory. Each plot should have a
        descriptive title that states what the distribution reveals.
    """
    # TODO: Create distribution plots for numeric columns like GPA,
    #       study hours, attendance, and commute minutes
    # TODO: Use histograms with KDE overlay (sns.histplot) or box plots
    # TODO: Save each plot to the output/ directory
    
    #Histograms with KDE for continuous variables (e.g., gpa, study_hours_weekly, attendance_pct) — use sns.histplot(kde=True)
    numeric_cols = ["gpa", "study_hours_weekly", "attendance_pct", "commute_minutes"]
    for col in numeric_cols:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col} (mean={df[col].mean():.2f})")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.savefig(f"output/{col}_distribution.png")
        plt.close()
    #Box plot comparing gpa across department — use sns.boxplot()
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="department", y="gpa", data=df)
    plt.title("GPA Distribution Across Departments")
    plt.xlabel("Department")
    plt.ylabel("GPA")
    plt.savefig("output/gpa_by_department.png")
    plt.close()

    #Bar chart for at least one categorical variable distribution (e.g., scholarship counts)
    plt.figure(figsize=(10, 6))
    sns.countplot(x="scholarship", data=df)
    plt.title("Distribution of Scholarship Recipients")
    plt.xlabel("Scholarship")
    plt.ylabel("Count")
    plt.savefig("output/scholarship_distribution.png")
    plt.close()

def plot_correlations(df):
    """Analyze and visualize relationships between numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least one correlation visualization to the output/ directory
        (e.g., a heatmap, scatter plot, or pair plot).
    """
    # TODO: Compute the correlation matrix for numeric columns
    # TODO: Create a heatmap or scatter plots showing key relationships
    # TODO: Save the visualization(s) to the output/ directory
    numeric_cols = ["gpa", "study_hours_weekly", "attendance_pct", "commute_minutes","course_load"]
    corr_matrix = df[numeric_cols].corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig("output/correlation_matrix.png")
    plt.close()
#Create scatter plots for the two most correlated variable pairs (excluding self-correlation)
    corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
    corr_pairs = corr_pairs[corr_pairs < 1]  # Exclude self-correlation
    top_pairs = corr_pairs.head(2).index.tolist()
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df[top_pairs[0][0]], y=df[top_pairs[0][1]])
    plt.title(f"Scatter Plot of {top_pairs[0][0]} vs {top_pairs[0][1]} (corr={corr_matrix.loc[top_pairs[0][0], top_pairs[0][1]]:.2f})")
    plt.xlabel(top_pairs[0][0])
    plt.ylabel(top_pairs[0][1])
    plt.savefig(f"output/scatter_{top_pairs[0][0]}_vs_{top_pairs[0][1]}.png")
    plt.close()
    #Document findings in your analysis: which variables are related, and what might explain the relationship?
    print("Findings:")
    print(f"- {top_pairs[0][0]} and {top_pairs[0][1]} are highly correlated (r={corr_matrix.loc[top_pairs[0][0], top_pairs[0][1]]:.2f})")


def run_hypothesis_tests(df):
    """Run statistical tests to validate observed patterns.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        dict: test results with keys like 'internship_ttest', 'dept_anova',
              each containing the test statistic and p-value

    Side effects:
        Prints test results to stdout with interpretation.

    Tests to consider:
        - t-test: Does GPA differ between students with and without internships?
        - ANOVA: Does GPA differ across departments?
        - Correlation test: Is the correlation between study hours and GPA significant?
    """
    # TODO: Run at least two hypothesis tests on patterns you observe in the data
    # TODO: Report the test statistic, p-value, and your interpretation
    #Use an independent samples t-test: scipy.stats.ttest_ind()
    #Report: t-statistic, p-value, and a plain-language interpretation
    #Compute Cohen’s d for effect size
    internship_gpa = df[df["has_internship"] == "Yes"]["gpa"]
    no_internship_gpa = df[df["has_internship"] == "No"]["gpa"]
    t_stat, p_value = stats.ttest_ind(internship_gpa, no_internship_gpa, equal_var=False)
    cohen_d = (internship_gpa.mean() - no_internship_gpa.mean()) / np.sqrt((internship_gpa.std() ** 2 + no_internship_gpa.std() ** 2) / 2)
    print("T-test: GPA by Internship Status")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Cohen's d: {cohen_d:.4f}\n")
    if p_value < 0.05:
        print("  Interpretation: There is a statistically significant difference in GPA between students with and without internships.\n")
    else:
        print("  Interpretation: There is no statistically significant difference in GPA between students with and without internships.\n")
    #Hypothesis 2: “Scholarship status is associated with department.”
    #Use a chi-square test: pd.crosstab() then scipy.stats.chi2_contingency()
    #Report: chi-square statistic, p-value, degrees of freedom, and a plain-language interpretation
    scholarship_dept_table = pd.crosstab(df["scholarship"], df["department"])
    chi2_stat, p_value, dof, expected = stats.chi2_contingency(scholarship_dept_table)
    print("Chi-square Test: Scholarship Status by Department")
    print(f"  chi-square statistic: {chi2_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  degrees of freedom: {dof}\n")
    if p_value < 0.05:
        print("  Interpretation: There is a statistically significant association between scholarship status and department.\n")
    else:
        print("  Interpretation: There is no statistically significant association between scholarship status and department.\n")
 # - ANOVA: Does GPA differ across departments?
    #Use one-way ANOVA: scipy.stats.f_oneway()
    #Report: F-statistic, p-value, and a plain-language interpretation
    dept_gpas = [df[df["department"] == dept]["gpa"] for dept in df["department"].unique()]
    f_stat, p_value = stats.f_oneway(*dept_gpas)
    print("ANOVA: GPA by Department")
    print(f"  F-statistic: {f_stat:.4f}")
    print(f"  p-value: {p_value:.4f}\n")
    if p_value < 0.05:
        print("  Interpretation: There is a statistically significant difference in GPA across departments.\n")
    else:
        print("  Interpretation: There is no statistically significant difference in GPA across departments.\n")


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)

    # TODO: Load and profile the dataset
    # TODO: Generate distribution plots
    # TODO: Analyze correlations
    # TODO: Run hypothesis tests
    # TODO: Write a FINDINGS.md summarizing your analysis
    df = load_and_profile("data/student_performance.csv")
    df = clean_data(df)
    plot_distributions(df)
    plot_correlations(df)
    run_hypothesis_tests(df)
if __name__ == "__main__":
    main()
