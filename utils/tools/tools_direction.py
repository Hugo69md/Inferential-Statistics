from utils.tools.hypothesis_testing.parametric_tests_t.two_samples_t_tests.two_samples_independant.eq_of_means import eq_of_means
from utils.tools.hypothesis_testing.parametric_tests_t.two_samples_t_tests.two_samples_paired.two_samples_paired import two_samples_paired
from utils.tools.hypothesis_testing.parametric_tests_t.one_sample_t_test.one_sample_t_test  import one_sample_t_test
from utils.tools.hypothesis_testing.non_parametric_tests.two_samples_non_param.mann_whitney_u import mann_whitney_u
from utils.tools.hypothesis_testing.non_parametric_tests.two_samples_non_param.two_samples_wilcoxon import two_samples_wilcoxon
from utils.tools.hypothesis_testing.non_parametric_tests.one_sample_non_param.one_sample_wilcoxon import one_sample_wilcoxon
from utils.tools.hypothesis_testing.distribution_tests.normality_test.one_sample.normality_test_one_sample import normality_test_one_sample
from utils.tools.hypothesis_testing.distribution_tests.normality_test.two_samples.normality_test_two_samples import normality_test_two_samples

def tools_direction(df, tool_selection, col1, col2):
    if tool_selection == 1:
        one_sample_t_test(df, col1)

    elif tool_selection == 2:
        choice = int(input("Paired t test or eq of means ? (1 for paired, 2 for eq of means)"))
        if choice == 1 : 
            two_samples_paired(df, col1, col2)
        elif choice == 2 : 
            eq_of_means(df, col1, col2)

    elif tool_selection == 3:
        one_sample_wilcoxon(df, col1)

    elif tool_selection == 4:
        choice = int(input("Dependant test or independant ? (1 for dependant, 2 indepandant)"))
        if choice == 1 : 
            two_samples_wilcoxon(df, col1, col2)
        elif choice == 2 : 
            mann_whitney_u(df, col1, col2)

    