import pandas as pd #type: ignore
import numpy as np #type: ignore
import seaborn as sns #type: ignore
import matplotlib.pyplot as plt  #type: ignore
import sys
from scipy import stats #type: ignore
from utils.tools.hypothesis_testing.distribution_tests.normality_test.two_samples.normality_test_two_samples import normality_test_two_samples
import os # type: ignore
import datetime #type: ignore
from utils.tools.hypothesis_testing.distribution_tests.skewness_kurtosis_tests.wilcoxon_assumptions.symmetry_test import symmetry_test
def two_samples_wilcoxon(df, col1, col2):
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
    between_directory_2 = os.path.join(between_directory_3, '2_samples_wilcoxon')
    subdirectory = os.path.join(between_directory_2, f'2_samples_wilcoxon_{timestamp}')
    os.makedirs(subdirectory)

    report_normality, reject_null_norm = normality_test_two_samples(array_list, samplesize1, samplesize2, alpha) # returns a report on the normality test, returns a tuple of boolean for normality of the dataset

    report_symmetry, reject_symmetry, differences = symmetry_test(alpha=alpha, col1=col1, col1array=col1array, col2=col2, col2array=col2array)

    #Perform a t-test on two datasets 
    t_stat, p_value = stats.wilcoxon(x = array_list[0], y = array_list[1]) 

    reject_str_var = "H0 accepted, the medians are equal" if p_value > alpha else "H1 accepted, the medians are not equal"

    median1 = np.median(col1array)  # Sample1 median
    median2 = np.median(col2array)  # Sample 2 median

    report = f"""
        /================== Dependant equality of Medians Test Results Wilcoxon signed rank ==================/
        Sample Size: {samplesize1}
        Alpha: {alpha}
        Method Used: 'Wilcoxon\'s 2 sample paired test 
        Test Statistic: {t_stat}
        P-Value: {p_value}
        Hypothesis testing for equality of medians: {reject_str_var}

        /============================ Medians infos ============================/
        Sample 1 Median: {median1:.6f}
        Sample 2 Median: {median2:.6f}

        /============================ Warnings ============================/
        {'!!!!!! the distribution of at least one sample is NORMAL, the results might not reflect reality' if any(reject_null_norm) else'//'}
        {'!!!!!! the sample is not symmetric, the results might not reflect reality' if not reject_symmetry else'//'}
        """
    finalreport = f"{report_normality} \n\n {report_symmetry} \n\n {report}"

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
    plt.title(f'Wilcoxon signed rank, Equality of medians between {col1} and {col2}')
    plt.grid(True, alpha=0.3)

    # Save first boxplot
    filename1 = os.path.join(subdirectory, f"boxplot_2_samples_wilcoxon_{col1}_&_{col2}_{timestamp}.png")
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

    #third graph for comparison
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
    filename3 = os.path.join(subdirectory, f"difference_and_Q-Q_plot_of_{col1}_&_{col2}_{timestamp}.png")
    plt.savefig(filename3, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory


    #save eq of medians report
    feedback_file = os.path.join(subdirectory, f'2_samples_wilcoxon_report_{timestamp}.txt')
    with open(feedback_file, 'w') as f:
        f.write(finalreport)