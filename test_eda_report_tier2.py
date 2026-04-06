"""
Tests for Automated EDA Report Generator
"""

import os
import pandas as pd
import numpy as np

from eda_report_tier2 import generate_eda_report


# =====================================================
# TEST 1 — basic dataframe
# =====================================================

def test_basic_dataframe():
    df = pd.DataFrame({
        "a": [1, 2, 3, 4, 5],
        "b": [5, 4, 3, 2, 1],
        "category": ["x", "y", "x", "y", "x"]
    })

    generate_eda_report(df, output_dir="test_output")

    assert os.path.exists("test_output/data_profile.txt")
    assert os.path.exists("test_output/missing_values.png")


# =====================================================
# TEST 2 — dataframe with missing values
# =====================================================

def test_missing_values():
    df = pd.DataFrame({
        "num1": [1, 2, np.nan, 4],
        "num2": [np.nan, 1, 2, 3]
    })

    generate_eda_report(df, output_dir="test_output_missing")

    assert os.path.exists("test_output_missing/outlier_summary.txt")


# =====================================================
# TEST 3 — different column types
# =====================================================

def test_mixed_types():
    df = pd.DataFrame({
        "numeric": np.random.randn(20),
        "integer": np.random.randint(0, 10, 20),
        "text": ["A"] * 20
    })

    generate_eda_report(df, output_dir="test_output_types")

    assert os.path.exists("test_output_types/correlation_heatmap.png")