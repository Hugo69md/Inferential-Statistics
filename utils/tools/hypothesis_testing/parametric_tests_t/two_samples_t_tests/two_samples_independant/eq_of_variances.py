from scipy import stats #type: ignore
import numpy as np #type: ignore
import matplotlib.pyplot as plt #type: ignore
import seaborn as sns #type: ignore
import os
import pandas as pd #type: ignore

def eq_of_variances(alpha, array_list, reject_null_norm, samplesize):
    
    col1array = array_list[0]
    col2array = array_list[1]

    # Determine which test to use based on the normality test results

    if all(reject_null_norm):  # If either sample is not normal
        print("Using Levene's test for equality of variances.")
        stat_var, p_value_var = stats.bartlett(col1array, col2array)
    else:
        print("Using Bartlett's test for equality of variances.")
        stat_var, p_value_var = stats.levene(col1array, col2array)

    # Determine if we can reject the null hypothesis
    reject_null_eq_var = p_value_var > alpha

    # Change the reject null bool to str for better comprehension in the report
    reject_str_var = "H0 accepted, the variances are equal" if reject_null_eq_var else "H1 accepted, the variances are not equal"

    # Calculate variances for visualization
    var1 = np.var(col1array, ddof=1)  # Sample1 variance
    var2 = np.var(col2array, ddof=1)  # Sample 2 variance
    var_ratio = max(var1, var2)/min(var1, var2)

    # Report on equality of variances test
    report = f"""
        /================== Equality of Variances Test Results ==================/
        Sample Size: {samplesize}
        Alpha: {alpha}
        Method Used: {'Bartlett\'s test' if all(reject_null_norm) else 'Levene\'s test'}
        Test Statistic: {stat_var}
        P-Value: {p_value_var}
        Hypothesis testing for equality of variances: {reject_str_var}

        /============================ Variance infos ============================/
        Sample 1 Variance: {var1:.6f}
        Sample 2 Variance: {var2:.6f}
        Variance Ratio (larger/smaller): {var_ratio:.4f}
    """

    return report, reject_null_eq_var