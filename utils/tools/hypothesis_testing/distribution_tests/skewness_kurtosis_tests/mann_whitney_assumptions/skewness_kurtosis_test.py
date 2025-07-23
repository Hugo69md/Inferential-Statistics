from scipy import stats #type: ignore
import numpy as np #type: ignore

def skewness_kurtosis_test(alpha, col1, col1array, col2, col2array, samplesize1):

    if samplesize1 < 100 : 
        tol = 0.2
    elif 100 < samplesize1 < 2000 : 
        tol = 0.3
    else :
        tol = 0.35

    # Compute skewness and kurtosis
    skew1 = stats.skew(col1array)
    skew2 = stats.skew(col2array)
    kurt1 = stats.kurtosis(col1array)
    kurt2 = stats.kurtosis(col2array)

    # Compare shape similarity using tolerance threshold
    skew_diff = abs(skew1 - skew2)
    kurt_diff = abs(kurt1 - kurt2)

    skew_similar = skew_diff < tol
    kurt_similar = kurt_diff < tol
    shape_similar_tuple = (skew_similar, kurt_similar)
    shape_similar = all(shape_similar_tuple)

    reject_str_var_general = (
        "H0 accepted: Distributions have similar shape (skewness and kurtosis)."
        if shape_similar else
        "H1 accepted: Distributions have different shape (skewness and/or kurtosis)."
    )
    reject_str_var_skew = (
        "H0 accepted: Distributions have similar skewness."
        if skew_similar else
        "H1 accepted: Distributions have different skewness."
    )
    reject_str_var_kurt = (
        "H0 accepted: Distributions have similar kurtosis."
        if shape_similar else
        "H1 accepted: Distributions have different kurtosis."
    )

    warning = (
        "!!!!!! WARNING: Distributions differ in shape — Mann-Whitney U assumptions may not hold."
        if not shape_similar else "//"
    )

    report = f"""
        /================== Distribution Shape Check for Mann-Whitney U ==================/
        Sample Names: {col1} vs {col2}
        Sample Sizes: {samplesize1}
        Alpha Level (informal): {alpha}
        Comparison Tolerance: {tol:.3f} (Depends on sample size)
        
        /============================ Skewness ============================/
        Skewness Sample 1 ({col1}): {skew1:.6f}
        Skewness Sample 2 ({col2}): {skew2:.6f}
        Absolute Difference: {skew_diff:.6f}
        Skewness similarity Decision: {reject_str_var_skew}

        /============================ Kurtosis ============================/
        Kurtosis Sample 1 ({col1}): {kurt1:.6f}
        Kurtosis Sample 2 ({col2}): {kurt2:.6f}
        Absolute Difference: {kurt_diff:.6f}
        Kurtosis similarity Decision: {reject_str_var_kurt}

        /============================ Decision ============================/
        Shape Similarity Decision: {reject_str_var_general}

        /============================ Warning ============================/
        {warning}
    """

    return report, shape_similar 