import pandas as pd #type: ignore
from utils.tools.hypothesis_testing.distribution_tests.normality_test.two_samples.sub_functions_norm_two_samp.shapiro_dagostino_two_samples import shapiro_dagostino_two_samples
from utils.tools.hypothesis_testing.distribution_tests.normality_test.two_samples.sub_functions_norm_two_samp.anderson_darling_two_samples import anderson_darling_two_samples
import numpy as np #type: ignore

def normality_test_two_samples(array_list, samplesize1, samplesize2, alpha):
    """
    Perform a normality test on the given data using different methods.qqq‡dq

    Shapiro wilk for samples less than 5000
    Anderson-Darling for samples greater than 5000 and alpha <= 0.05
    d'agostino for samples greater than 5000 and alpha > 0.05

    this function will return the test statistic, p-value, and whether the null hypothesis can be rejected.
    it will also return a f string explaining which method was used for the normality test. and the additional information about this very test

    """
    #extract data
    col1array = array_list[0]
    col2array = array_list[1]

    # Get the data from the columns
    if samplesize1 != samplesize2:
        raise ValueError("For ease of comparison, The two columns must have the same number of samples for the normality test.")
    
    # Check if the sample size is less than 5000
    if (samplesize1 < 5000) or (samplesize1 >= 5000 and alpha > 0.05):
        #shapiro or dagostino cases
        report_norm_test, reject_null_norm = shapiro_dagostino_two_samples(alpha, samplesize1, col1array, col2array)
    else:
        #anderson darling case
        report_norm_test, reject_null_norm = anderson_darling_two_samples(alpha, samplesize1, col1array, col2array)
    
    return report_norm_test , reject_null_norm
