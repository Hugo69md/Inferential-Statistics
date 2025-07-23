import pandas as pd # type: ignore
import numpy as np #type: ignore
from utils.tools.hypothesis_testing.distribution_tests.normality_test.one_sample.sub_functions_norm_one_samp.shapiro_dagostino_one_sample import shapiro_dagostino_one_sample
from utils.tools.hypothesis_testing.distribution_tests.normality_test.one_sample.sub_functions_norm_one_samp.anderson_darling_one_sample import anderson_darling_one_sample

def normality_test_one_sample(sample, samplesize, alpha):
    """
    Perform a normality test on the given data using different methods.qqq‡dq

    Shapiro wilk for samples less than 5000
    Anderson-Darling for samples greater than 5000 and alpha <= 0.05
    d'agostino for samples greater than 5000 and alpha > 0.05

    this function will return the test statistic, p-value, and whether the null hypothesis can be rejected.
    it will also return a f string explaining which method was used for the normality test. and the additional information about this very test

    """
    
    # Check if the sample size is less than 5000
    if (samplesize < 5000) or (samplesize >= 5000 and alpha > 0.05):
        #shapiro or dagostino cases
        report , reject_null = shapiro_dagostino_one_sample(alpha, samplesize, sample)
    else:
        #anderson darling case
        report , reject_null = anderson_darling_one_sample(alpha, samplesize, sample)

    return report , reject_null