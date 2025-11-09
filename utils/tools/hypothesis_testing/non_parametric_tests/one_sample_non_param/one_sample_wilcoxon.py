import pandas as pd #type: ignore
import numpy as np #type: ignore
import seaborn as sns #type: ignore
import matplotlib.pyplot as plt #type: ignore
from scipy import stats #type: ignore
import datetime
import os
from utils.tools.hypothesis_testing.distribution_tests.normality_test.one_sample.normality_test_one_sample import normality_test_one_sample
from utils.tools.hypothesis_testing.distribution_tests.skewness_kurtosis_tests.wilcoxon_assumptions.symmetry_test import symmetry_test
def one_sample_wilcoxon(df, col1):
    #import data
    sample = df[col1].to_numpy()
    samplesize = df[col1].count()
    median = float(input("Enter the population median for the wilcoxon 1 sample test (e.g., 54.87 / 298.5 / 40): ").replace(',', '.'))

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
    between_directory_2 = os.path.join(between_directory, '1_sample_wilcoxon')
    subdirectory = os.path.join(between_directory_2, f'1_sample_wilcoxon_{timestamp}')
    os.makedirs(subdirectory)

    report_norm, reject_null_norm = normality_test_one_sample(sample, samplesize, alpha)

    report_symmetry, reject_symmetry, differences = symmetry_test(alpha=alpha, col1=col1, col1array=sample, median=median)

    """Perform a wilcoxon 1 sample test on the dataset."""
    t_stat, p_value = stats.wilcoxon(sample - median)   # Assuming a population median of 54 for the test
    print(f"T-statistic: {t_stat}, P-value: {p_value}")

    #Interpret the results of the hypothesis test.
    reject_str_var = "H0 accepted, the means are equal" if p_value > alpha else "H1 accepted, the means are not equal"    

    #report on the test
    report = f"""
        /================== 1 sample Wilcoxon Test Results ==================/
        Sample Size: {samplesize}
        Alpha: {alpha}
        Method Used: 'Wilcoxon\'s 1 sample test
        Test Statistic: {t_stat}
        P-Value: {p_value}
        Expected Median: {median}
        Hypothesis testing: {reject_str_var}

        /============================ Warnings ============================/
        {'!!!!!! the distribution is normal, Use 1 sample t-test for more accurate results' if reject_null_norm else'//'}
        {'!!!!!! the sample is not symmetric, the results might not reflect reality' if not reject_symmetry else'//'}

        """
    finalreport = f"{report_norm} \n\n {report_symmetry} \n\n {report}"

    print(finalreport)
    """Plot the data using box plots with Seaborn."""
    # Combine the data into a single DataFrame for easier plotting with Seaborn
    newdf = pd.DataFrame({
        'Values': np.concatenate([sample]),
        'Sample': [col1] * len(sample) })
    
    # Create a box plot using Seaborn
    plt.figure(figsize=(12, 10))  # Create new figure for first plot
    sns.boxplot(x='Sample', y='Values', data=newdf, color='skyblue')
    plt.axhline(y=median,  color='red', linestyle='--')
    plt.title(f'Wilcoxon 1 Sample test for {col1}')
    plt.grid(True, alpha=0.3)

    # Save first boxplot
    filename1 = os.path.join(subdirectory, f"boxplot_1_sample_wilcoxon_{col1}_{timestamp}.png")
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

    #show differences graph and Q-Q plot
    differences_reworked = pd.Series(differences)  # for easier integration with seaborn
    plt.figure(figsize=(12, 5))

    # Histogram with KDE
    plt.subplot(1, 2, 1)
    sns.histplot(differences_reworked, bins=10, kde=True, color='skyblue', edgecolor='black')
    plt.axvline(0, color='red', linestyle='--')
    plt.title("Histogram of Differences")

    # Q-Q Plot
    plt.subplot(1, 2, 2)
    stats.probplot(differences_reworked, dist="norm", plot=plt)
    plt.title("Q-Q Plot")

    # Save difference graph
    filename3 = os.path.join(subdirectory, f"difference_and_Q-Q_plot_of_{col1}_{timestamp}.png")
    plt.savefig(filename3, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory


    #save eq of means report
    feedback_file = os.path.join(subdirectory, f'1_sample_wilcoxon_test_report_{timestamp}.txt')
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