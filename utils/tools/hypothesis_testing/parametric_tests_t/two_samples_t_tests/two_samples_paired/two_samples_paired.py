import pandas as pd #type: ignore
import numpy as np #type: ignore
import seaborn as sns #type: ignore
import matplotlib.pyplot as plt  #type: ignore
import sys
from scipy import stats #type: ignore
from utils.tools.hypothesis_testing.distribution_tests.normality_test.two_samples.normality_test_two_samples import normality_test_two_samples
import os # type: ignore
import datetime #type: ignore

def two_samples_paired(df, col1, col2):
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
    between_directory_3 = os.path.join(between_directory, 'dependant')
    between_directory_2 = os.path.join(between_directory_3, '2_samples_paired_t')
    subdirectory = os.path.join(between_directory_2, f'2_samples_paired_t_{timestamp}')
    os.makedirs(subdirectory)

    report_normality, reject_null_norm = normality_test_two_samples(array_list, samplesize1, samplesize2, alpha) # returns a report on the normality test, returns a tuple of boolean for normality of the dataset

    #Perform a t-test on two datasets 
    t_stat, p_value = stats.ttest_rel(array_list[0], array_list[1]) 

    reject_str_var = "H0 accepted, the means are equal" if p_value > alpha else "H1 accepted, the means are not equal"

    mean1 = np.mean(col1array)  # Sample1 mean
    mean2 = np.mean(col2array)  # Sample 2 mean

    report = f"""
        /================== Dependant equality of Means Test Results ==================/
        Sample Size: {samplesize1}
        Alpha: {alpha}
        Method Used: 'Student\'s 2 sample paired T test
        Test Statistic: {t_stat}
        P-Value: {p_value}
        Hypothesis testing for equality of means: {reject_str_var}

        /============================ Means infos ============================/
        Sample 1 Mean: {mean1:.6f}
        Sample 2 Mean: {mean2:.6f}

        /============================ Warnings ============================/
        {'!!!!!! the distribution of at least one sample is NOT normal, use a non parametric test' if not all(reject_null_norm) else'//'}
        """
    finalreport = f"{report_normality} \n\n {report}"

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
    plt.title(f'Dependant Equality of means between {col1} and {col2}')
    plt.grid(True, alpha=0.3)

    # Save first boxplot
    filename1 = os.path.join(subdirectory, f"boxplot_dependant_eq_of_means_{col1}_&_{col2}_{timestamp}.png")
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

    #save eq of means report
    feedback_file = os.path.join(subdirectory, f'dependant_eq_of_means_report_{timestamp}.txt')
    with open(feedback_file, 'w') as f:
        f.write(finalreport)