"""
Tier 3 — Statistical Simulation and Power Analysis
"""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower


# =====================================================
# 1. BOOTSTRAP CONFIDENCE INTERVAL
# =====================================================

def bootstrap_ci(data, n_bootstrap=10000, ci=95):
    """
    Compute bootstrap confidence interval for the mean.
    """

    means = []

    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        means.append(np.mean(sample))

    lower = np.percentile(means, (100 - ci) / 2)
    upper = np.percentile(means, 100 - (100 - ci) / 2)

    return lower, upper


def compare_bootstrap_vs_ttest(df):
    """
    Compare bootstrap CI with parametric t-test CI.
    """

    with_int = df[df["has_internship"] == "Yes"]["gpa"].dropna()
    without_int = df[df["has_internship"] == "No"]["gpa"].dropna()

    # ---------- Bootstrap ----------
    boot_ci_yes = bootstrap_ci(with_int)
    boot_ci_no = bootstrap_ci(without_int)

    # ---------- Parametric CI ----------
    def ttest_ci(sample):
        mean = np.mean(sample)
        sem = stats.sem(sample)
        ci = stats.t.interval(
            0.95,
            len(sample) - 1,
            loc=mean,
            scale=sem
        )
        return ci

    t_ci_yes = ttest_ci(with_int)
    t_ci_no = ttest_ci(without_int)

    print("\nBootstrap CI (Internship):", boot_ci_yes)
    print("T-test CI (Internship):", t_ci_yes)

    print("\nBootstrap CI (No Internship):", boot_ci_no)
    print("T-test CI (No Internship):", t_ci_no)


# =====================================================
# 2. POWER ANALYSIS
# =====================================================

def power_analysis(effect_size, alpha=0.05, power=0.8):
    """
    Compute required sample size.
    """

    analysis = TTestIndPower()

    sample_size = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        alternative="two-sided"
    )

    print("\nRequired sample size per group:", int(np.ceil(sample_size)))

    return sample_size


# =====================================================
# 3. STATISTICAL SIMULATION
# =====================================================

def false_positive_simulation(
    n_simulations=1000,
    sample_size=30,
    alpha=0.05
):
    """
    Simulate hypothesis testing under NULL hypothesis
    and measure false positive rate.
    """

    false_positives = 0

    for _ in range(n_simulations):

        # generate identical distributions (H0 true)
        group1 = np.random.normal(3.0, 0.3, sample_size)
        group2 = np.random.normal(3.0, 0.3, sample_size)

        _, p_value = stats.ttest_ind(group1, group2)

        if p_value < alpha:
            false_positives += 1

    rate = false_positives / n_simulations

    print("\nFalse Positive Rate:", rate)
    print("Expected alpha:", alpha)

    return rate


# =====================================================
# MAIN RUNNER
# =====================================================

def run_tier3(df, effect_size):
    print("\n========== TIER 3 ANALYSIS ==========")

    compare_bootstrap_vs_ttest(df)

    power_analysis(effect_size)

    false_positive_simulation()


if __name__ == "__main__":
    print("Import this module and call run_tier3(df, effect_size)")