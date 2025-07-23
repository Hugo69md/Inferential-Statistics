from scipy import stats #type: ignore
import numpy as np #type: ignore
def symmetry_test(alpha, col1, col1array, col2=None, col2array=None, median=None):

    is_symmetric = None
    
    if col2array is None : 
        differences = col1array - median
        skew_stat, p_value = stats.skewtest(differences)

        if p_value > alpha:
            is_symmetric = True
        else:
            is_symmetric = False
        
    else : 
        differences = col1array - col2array
        skew_stat, p_value = stats.skewtest(differences)

        if p_value > alpha:
            is_symmetric = True
        else:
            is_symmetric = False
    
    reject_str_var = "H0 accepted, data is likely symmetric" if is_symmetric else "H1 accepted, data is likely asymmetric"
    warning = "!!!!!! WARNING: Data is significantly skewed — Wilcoxon test assumptions may not hold." if not is_symmetric else "//"
    sample_name = f"{col1} & {col2}" if col2array is not None else f"{col1}"
    skew_value = np.mean(differences)  # optional: could show mean for context

    report = f"""
        /====================== Symmetry Test Results Using Skewness ======================/
        Sample Name: {sample_name}
        Sample Size (non-zero diffs): {len(differences)}
        Alpha Level: {alpha}
        Method Used: 'Skewness Test' (scipy.stats.skewtest)
        Test Statistic: {skew_stat:.6f}
        P-Value: {p_value:.6f}
        Symmetry Decision: {reject_str_var}
    
        /============================ Difference Distribution Info ============================/
        Mean of Differences: {skew_value:.6f}
        Median of Differences: {np.median(differences):.6f}
        Min / Max: {np.min(differences):.6f} / {np.max(differences):.6f}

        /=================================== Warnings ===================================/
        {warning}
        """

    return report, is_symmetric, differences
