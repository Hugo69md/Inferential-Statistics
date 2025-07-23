from scipy import stats # type: ignore

def shapiro_dagostino_one_sample(alpha, samplesize, sample):

    if (samplesize < 5000):
        reportvar = 0
        print("Using Shapiro-Wilk test for normality.")
        stat_norm, p_value_norm = stats.shapiro(sample)
    else :
        reportvar = 1
        print("Using D'Agostino's K-squared test for normality.")
        stat_norm, p_value_norm = stats.normaltest(sample)

    # Determine if we can reject the null hypothesis
    reject_null = p_value_norm > alpha

    #Change the reject null bool by str for better comprehension on the report
    reject_str = ("H0 accepted, normality test validated" if reject_null else "H1 accepted, normality test not validated")

    #report on normality test
    report =  f"""
        /================== Normality Test Results ==================/
        Sample Size: {samplesize}
        Alpha: {alpha}
        Method Used: {'Shapiro-Wilk (Sample size <= 5000)' if reportvar == 0 else 'D\'Agostino\'s K-squared (Sample size > 5000 && alpha >= 0,05)'}

        /================== Sample analysis ==================/
        Test Statistic sample : {stat_norm}
        P-Value: {p_value_norm}
        Hypothesis testing for normality test results: {reject_str}
        """
    return report, reject_null