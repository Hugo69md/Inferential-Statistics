import pandas as pd #type: ignore
import numpy as np #type: ignore
import seaborn as sns #type: ignore
import matplotlib.pyplot as plt  #type: ignore
import sys
from scipy import stats #type: ignore
from utils.tools.hypothesis_testing.distribution_tests.normality_test.two_samples.normality_test_two_samples import normality_test_two_samples
from utils.tools.hypothesis_testing.distribution_tests.skewness_kurtosis_tests.mann_whitney_assumptions.skewness_kurtosis_test import skewness_kurtosis_test
import os # type: ignore
import datetime #type: ignore

def mann_whitney_u(df, col1, col2):
     # Extract the column sample size 
    samplesize1 = df[col1].count()
    samplesize2 = df[col2].count()

    # convert to np array
    col1array = df[col1].to_numpy()
    col2array = df[col2].to_numpy()

    array_list = [col1array, col2array]

    try:
        alpha = input ("Enter alpha for the t-test default is 0.05. use numbers ranging from 0 to 100: ")
        alpha = float(alpha) / 100 # Convert percentage to decimal
        if alpha < 0 or alpha > 1: # superior to 1?
            raise ValueError("Alpha must be between 0 and 100.")
        
    except ValueError:  
        print("Invalid input for alpha. Using default value of 0.05.")
        alpha = 0.05

    #create directory for outputs
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") #timestamp do differ every files
    directory = 'outputs'
    between_directory = os.path.join(directory, '2_samples')
    between_directory_3 = os.path.join(between_directory, 'independant')
    between_directory_2 = os.path.join(between_directory_3, '2_samples_mann_whitney')
    subdirectory = os.path.join(between_directory_2, f'2_samples_mann_whitney_{timestamp}')
    os.makedirs(subdirectory)

    report_normality, reject_null_norm = normality_test_two_samples(array_list, samplesize1, samplesize2, alpha) # returns a report on the normality test, returns a tuple of boolean for normality of the dataset

    report_shape, is_shape_similar = skewness_kurtosis_test(alpha, col1, col1array, col2, col2array, samplesize1)
    #Perform a t-test on two datasets 
    t_stat, p_value = stats.ranksums(x = array_list[0], y = array_list[1]) 

    reject_str_var = "H0 accepted, the medians are equal" if p_value > alpha else "H1 accepted, the medians are not equal"

    median1 = np.median(col1array)  # Sample1 median
    median2 = np.median(col2array)  # Sample 2 median

    report = f"""
        /============ Independant equality of Medians Test Results Mann Whitney U rank sums ============/
        Sample Size: {samplesize1}
        Alpha: {alpha}
        Method Used: 'Mann Whitney\'s 2 sample Independant test
        Test Statistic: {t_stat}
        P-Value: {p_value}
        Hypothesis testing for equality of medians: {reject_str_var}

        /============================ Medians infos ============================/
        Sample 1 Median: {median1:.6f}
        Sample 2 Median: {median2:.6f}

        /============================ Warnings ============================/
        {'!!!!!! the distribution of at least one sample is NORMAL, the results might not reflect reality' if any(reject_null_norm) else'//'}
        {'!!!!!! the sample distribution are not alike, the results might not reflect reality' if not is_shape_similar else'//'}
        """
    finalreport = f"{report_normality} \n\n {report_shape} \n\n {report}"

    print(finalreport)
    """Plot the data using box plots with Seaborn."""
    # Combine the data into a single DataFrame for easier plotting with Seaborn
    newdf = pd.DataFrame({
        'Values': np.concatenate([array_list[0], array_list[1]]),
        'Samples': [col1] * len(array_list[0]) + [col2] * len(array_list[1])
    })
    
    # Create a box plot using Seaborn
    plt.figure(figsize=(12, 10))  # Create new figure for first plot
    sns.boxplot(x='Samples', y='Values', data=newdf, hue='Samples', palette=['skyblue', 'lightcoral'])
    plt.title(f'Mann Whitney U rank sums, Equality of medians between {col1} and {col2}')
    plt.grid(True, alpha=0.3)

    # Save first boxplot
    filename1 = os.path.join(subdirectory, f"boxplot_2_samples_mann_whitney_u_{col1}_&_{col2}_{timestamp}.png")
    plt.savefig(filename1, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory

    # create distribution plot using seaborn
    plt.figure(figsize=(24, 20))  # Create new figure for second plot
    sns.displot(data=newdf, x='Values', hue='Samples', kde=True, alpha = 0.6, fill=True, palette=['skyblue', 'lightcoral'])
    plt.title(f'Distribution of {col1} and {col2}')
    plt.grid(True, alpha=0.3)

    # Save second boxplot
    filename2 = os.path.join(subdirectory, f"distribution_plot_samples_{col1}_&_{col2}_{timestamp}.png")
    plt.savefig(filename2, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory

    #save eq of medians report
    feedback_file = os.path.join(subdirectory, f'2_samples_mann_whitney_u_report_{timestamp}.txt')
    with open(feedback_file, 'w') as f:
        f.write(finalreport)