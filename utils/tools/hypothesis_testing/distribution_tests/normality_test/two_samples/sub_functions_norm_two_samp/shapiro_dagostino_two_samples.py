from scipy import stats # type: ignore

def shapiro_dagostino_two_samples(alpha, samplesize1, col1array, col2array):

    if (samplesize1 <= 5000):
        reportvar = 0
        print("Using Shapiro-Wilk test for normality.")
        stat_norm_first_sample, p_value_norm_first_sample = stats.shapiro(col1array)
        stat_norm_second_sample, p_value_norm_second_sample = stats.shapiro(col2array)
    else :
        reportvar = 1
        print("Using D'Agostino's K-squared test for normality.")
        stat_norm_first_sample, p_value_norm_first_sample = stats.normaltest(col1array)
        stat_norm_second_sample, p_value_norm_second_sample = stats.normaltest(col2array)

    # Combine the results into tuples
    stat_norm = (stat_norm_first_sample, stat_norm_second_sample)
    p_value_norm = (p_value_norm_first_sample, p_value_norm_second_sample)
    # Determine if we can reject the null hypothesis
    reject_null_first_sample = p_value_norm[0] > alpha
    reject_null_second_sample = p_value_norm[1] > alpha
    # Combine the reject null results into a tuple
    reject_null = (reject_null_first_sample, reject_null_second_sample)

    #Change the reject null bool by str for better comprehension on the report
    reject_str = tuple(
    "H0 accepted, normality test validated" if reject_null[i] else "H1 accepted, normality test not validated"
    for i in range(2))

    #report on normality test
    report =  f"""
        /================== Normality Test Results ==================/
        Sample Size: {samplesize1}
        Alpha: {alpha}
        Method Used: {'Shapiro-Wilk (Sample size <= 5000)' if reportvar == 0 else 'D\'Agostino\'s K-squared (Sample size > 5000 && alpha >= 0,05)'}

        /================== First sample analysis ==================/
        Test Statistic first sample : {stat_norm[0]}
        P-Value: {p_value_norm[0]}
        Hypothesis testing for normality test results: {reject_str[0]}

        /================== Second sample analysis ==================/
        Test Statistic first sample : {stat_norm[1]}
        P-Value: {p_value_norm[1]}
        Hypothesis testing for normality test results: {reject_str[1]}
        """
    
    return report, reject_null