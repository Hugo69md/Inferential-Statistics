from scipy import stats # type: ignore
import numpy as np #type: ignore

def anderson_darling_one_sample(alpha, samplesize, sample):
    
    print("Using Anderson-Darling test for normality.")
    results = stats.anderson(sample, dist='norm')
    
    #extract results
    stat_norm = results.statistic
    crit_values = results.critical_values
    significance_level = results.significance_level


    # find correct significance level for the selected alpha
    index_next = next(i for i, level in enumerate(significance_level) if level <= (alpha*100)) #find correct significance level for given alpha 
    index_before = index_next - 1 #find correct significance level for given alpha (alpha is *100 bc the significance lvl outputs are in between 0 and 100)
    indexes_of_sig_lvl = (index_before, index_next)
    print(indexes_of_sig_lvl)

    #finding corect alpha
    if alpha * 100 <= 1:
        print(f"Alpha {alpha}% is too low; using the lowest available significance level (1%).")
        desired_alpha = 1
        interpolated_critical_value = crit_values[-1]

    elif alpha * 100 == 5:
        interpolated_critical_value = crit_values[2]
    
    elif alpha * 100 == 2.5:
        interpolated_critical_value = crit_values[3]

    else:
        # Interpolate to find the critical value for the specified alpha
        desired_alpha = alpha * 100
        siglvl_fsample_below = significance_level[0][indexes_of_sig_lvl[0]] 
        siglvl_fsample_above = significance_level[0][indexes_of_sig_lvl[1]]
        critval_fsample_below = crit_values[0][indexes_of_sig_lvl[0]]
        critval_fsample_above = crit_values[0][indexes_of_sig_lvl[1]]

        #aggregate into lists
        siglvl_fsample = [siglvl_fsample_above, siglvl_fsample_below] # arrays crit values and sig level are in descending order, must invert above and below for the interp function to work properly
        critval_fsample = [critval_fsample_above, critval_fsample_below]

        interpolated_critical_value = np.interp(desired_alpha, siglvl_fsample , critval_fsample)

    # Determine if we can reject the null hypothesis
    reject_null = stat_norm < interpolated_critical_value #null hypothesis accepted if stat_norm < crit value (rejected iff stat_norm > crit value)

    #Change the reject null bool by str for better comprehension on the report
    reject_str = (
    "H0 accepted, normality test validated" if reject_null else "H1 accepted, normality test not validated"
    )

    #report on normality test
    report = f"""
        /================== Normality Test Results ==================/
        Sample Size: {samplesize}
        Alpha: {alpha}
        Method Used: Anderson-Darling (samplesize >= 5000 && alpha <= 0,05)

        /================== Sample analysis ==================/
        Test Statistic first sample : {stat_norm}
        Critical Value accepted: {interpolated_critical_value}
        Hypothesis testing for normality test results: {reject_str}
        """
    
    return report, reject_null