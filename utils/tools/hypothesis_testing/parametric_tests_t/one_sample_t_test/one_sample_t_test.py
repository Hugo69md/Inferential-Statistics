import pandas as pd #type: ignore
import numpy as np #type: ignore
import seaborn as sns #type: ignore
import matplotlib.pyplot as plt #type: ignore
from scipy import stats #type: ignore
import datetime
import os
from utils.tools.hypothesis_testing.distribution_tests.normality_test.one_sample.normality_test_one_sample import normality_test_one_sample

def one_sample_t_test(df, col1):
    #import data
    sample = df[col1].to_numpy()
    samplesize = df[col1].count()
    mean = float(input("Enter the population mean for the t-test (e.g., 54.87 / 298.5 / 40): "))
    samplemean = np.mean(sample)
    # ask for alpha 
    try:
        alpha = input ("Enter alpha for the t-test default is 0.05. use numbers ranging from 0 to 100: ")
        alpha = float(alpha) / 100 # Convert percentage to decimal
        if alpha < 0 or alpha > 1: # superior to 1?
            raise ValueError("Alpha must be between 0 and 100.")
        
    except ValueError:  
        print("Invalid input for alpha. Using default value of 0.05.")
        alpha = 0.05

    #makedirectory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") #timestamp do differ every files
    directory = 'outputs'
    between_directory = os.path.join(directory, '1_sample')
    between_directory_2 = os.path.join(between_directory, '1_sample_t')
    subdirectory = os.path.join(between_directory_2, f'1_sample_t_{timestamp}')
    os.makedirs(subdirectory)

    report_norm, reject_null_norm = normality_test_one_sample(sample, samplesize, alpha)

    """Perform a t-test on two datasets."""
    t_stat, p_value = stats.ttest_1samp(sample, mean)  # Assuming a population mean of 54 for the test
    print(f"T-statistic: {t_stat}, P-value: {p_value}")

    #Interpret the results of the hypothesis test.
    reject_str_var = "H0 accepted, the expected mean correlates to the sample's mean" if p_value > alpha else "H1 accepted, the expected mean does not correlate to the sample's mean"    

    #report on the test
    report = f"""
        /================== 1 sample t-Test Results ==================/
        Sample Size: {samplesize}
        Alpha: {alpha}
        Method Used: 'Student\'s 1 sample T test
        Test Statistic: {t_stat}
        P-Value: {p_value}
        Expected Mean: {mean}
        Computed Mean: {samplemean}
        Hypothesis testing: {reject_str_var}

        /============================ Warnings ============================/
        {'!!!!!! the distribution is NOT normal, the results might not reflect reality' if not reject_null_norm else'//'}
        

        """
    finalreport = f"{report_norm} \n\n {report}"
    print(finalreport)
    """Plot the data using box plots with Seaborn."""
    # Combine the data into a single DataFrame for easier plotting with Seaborn
    newdf = pd.DataFrame({
        'Values': np.concatenate([sample]),
        'Sample': [col1] * len(sample) })
    
    # Create a box plot using Seaborn
    plt.figure(figsize=(12, 10))  # Create new figure for first plot
    sns.boxplot(x='Sample', y='Values', data=newdf, color='skyblue')
    plt.axhline(y=mean, color='red', linestyle='--')
    plt.title(f'1 Sample Student t test for {col1}')
    plt.grid(True, alpha=0.3)

    # Save first boxplot
    filename1 = os.path.join(subdirectory, f"boxplot_1_sample_t_{col1}_{timestamp}.png")
    plt.savefig(filename1, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory

    # create distribution plot using seaborn
    plt.figure(figsize=(24, 20))  # Create new figure for second plot
    sns.displot(data=newdf, x='Values', kde=True, alpha = 0.6, fill=True, color='lightcoral')
    plt.title(f'Distribution of {col1}')
    plt.grid(True, alpha=0.3)

    # Save second boxplot
    filename2 = os.path.join(subdirectory, f"distribution_plot_of_{col1}_{timestamp}.png")
    plt.savefig(filename2, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory

    #save eq of means report
    feedback_file = os.path.join(subdirectory, f'1_sample_t_test_report_{timestamp}.txt')
    with open(feedback_file, 'w') as f:
        f.write(finalreport)
# need to add a alpha parameter to the function
# to allow the user to set the significance level
# to allow the user to set the equal variance assumption
# diferent types of t-test
# add a report with the results of the hypothesis test
# add the graph to repo 
#corriger es trucs de add_strategy_2 et strategy 1

"""maybe"""
# and also to add a parameter to allow the user to set the alternative hypothesis 
# to allow the user to set the alternative hypothesis
# and also to add a parameter to allow the user to set the confidence interval
# to allow the user to set the confidence interval