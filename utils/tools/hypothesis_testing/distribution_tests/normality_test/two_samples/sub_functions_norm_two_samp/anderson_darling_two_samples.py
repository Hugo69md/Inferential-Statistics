from scipy import stats # type: ignore
import numpy as np #type: ignore

def anderson_darling_two_samples(alpha, samplesize1, col1array, col2array):
    
    print("Using Anderson-Darling test for normality.")
    result_first_sample = stats.anderson(col1array, dist='norm')
    result_second_sample = stats.anderson(col2array, dist='norm')

    #extract results
    stat_norm_first_sample = result_first_sample.statistic
    crit_values_norm_first_sample = result_first_sample.critical_values
    significance_level_first_sample = result_first_sample.significance_level

    stat_norm_second_sample = result_second_sample.statistic
    crit_values_norm_second_sample = result_second_sample.critical_values
    significance_level_second_sample = result_second_sample.significance_level

    # Combine the results into tuples
    stat_norm = (stat_norm_first_sample, stat_norm_second_sample) #tuple of single values
    crit_values_norm = (crit_values_norm_first_sample, crit_values_norm_second_sample) #tuple of lists of crit values
    significance_level =(significance_level_first_sample, significance_level_second_sample) #tuple of list of significance levels

    # find correct significance level for the selected alpha
    index_next = next(i for i, level in enumerate(significance_level[0]) if level <= (alpha*100)) #find correct significance level for given alpha 
    index_before = index_next - 1 #find correct significance level for given alpha (alpha is *100 bc the significance lvl outputs are in between 0 and 100)
    indexes_of_sig_lvl = (index_before, index_next)
    print(indexes_of_sig_lvl)

    #finding corect alpha
    if alpha * 100 <= 1:
        print(f"Alpha {alpha}% is too low; using the lowest available significance level (1%).")
        desired_alpha = 1
        interpolated_critical_values = (crit_values_norm_first_sample[-1], crit_values_norm_second_sample[-1])

    elif alpha * 100 == 5:
        interpolated_critical_values = (crit_values_norm_first_sample[2], crit_values_norm_second_sample[2])
    
    elif alpha * 100 == 2.5:
        interpolated_critical_values = (crit_values_norm_first_sample[3], crit_values_norm_second_sample[3])

    else:
        # Interpolate to find the critical value for the specified alpha
        desired_alpha = alpha * 100
        siglvl_fsample_below = significance_level[0][indexes_of_sig_lvl[0]] 
        siglvl_fsample_above = significance_level[0][indexes_of_sig_lvl[1]]
        critval_fsample_below = crit_values_norm[0][indexes_of_sig_lvl[0]]
        critval_fsample_above = crit_values_norm[0][indexes_of_sig_lvl[1]]
        siglvl_ssample_below = significance_level[1][indexes_of_sig_lvl[0]] 
        siglvl_ssample_above = significance_level[1][indexes_of_sig_lvl[1]]
        critval_ssample_below = crit_values_norm[1][indexes_of_sig_lvl[0]]
        critval_ssample_above = crit_values_norm[1][indexes_of_sig_lvl[1]]

        #aggregate into lists
        siglvl_fsample = [siglvl_fsample_above, siglvl_fsample_below] # arrays crit values and sig level are in descending order, must invert above and below for the interp function to work properly
        critval_fsample = [critval_fsample_above, critval_fsample_below]
        siglvl_ssample = [siglvl_ssample_above, siglvl_ssample_below,]
        critval_ssample = [ critval_ssample_above, critval_ssample_below]

        interpolated_crit_val_first_sample = np.interp(desired_alpha, siglvl_fsample , critval_fsample)
        interpolated_crit_val_second_sample = np.interp(desired_alpha, siglvl_ssample, critval_ssample)
        interpolated_critical_values = (interpolated_crit_val_first_sample, interpolated_crit_val_second_sample)

    # Determine if we can reject the null hypothesis
    reject_null_first_sample = stat_norm[0] < interpolated_critical_values[0] #null hypothesis accepted if stat_norm < crit value (rejected iff stat_norm > crit value)
    reject_null_second_sample = stat_norm[1] < interpolated_critical_values[1] 

    # Combine the reject null results into a tuple
    reject_null = (reject_null_first_sample, reject_null_second_sample)

    #Change the reject null bool by str for better comprehension on the report
    reject_str = tuple(
    "H0 accepted, normality test validated" if reject_null[i] else "H1 accepted, normality test not validated"
    for i in range(2))

    #report on normality test
    report = f"""
        /================== Normality Test Results ==================/
        Sample Size: {samplesize1}
        Alpha: {alpha}
        Method Used: Anderson-Darling (samplesize >= 5000 && alpha <= 0,05)

        /================== First sample analysis ==================/
        Test Statistic first sample : {stat_norm[0]}
        Critical Value accepted: {interpolated_critical_values[0]}
        Hypothesis testing for normality test results: {reject_str[0]}

        /================== Second sample analysis ==================/
        Test Statistic first sample : {stat_norm[1]}
        Critical Value accepted: {interpolated_critical_values[1]}
        Hypothesis testing for normality test results: {reject_str[1]}
        """
    
    return report, reject_null