import numpy as np #type: ignore
import pandas as pd #type: ignore

# Set seed for reproducibility
np.random.seed(42)

# Number of values
num_values = 5100

# Generate data for each column
uniform_data = np.random.uniform(0, 1, num_values)
logistic_data = np.random.logistic(0, 1, num_values)
normal_data = np.random.normal(0, 1, num_values)
gamma_data = np.random.gamma(1, 1, num_values)
beta_data = np.random.beta(1, 1, num_values)
chi_square_data = np.random.chisquare(5, num_values)
random_integers = np.random.randint(0, 51, num_values)

# Create a DataFrame
df = pd.DataFrame({
    'Uniform': uniform_data,
    'Logistic': logistic_data,
    'Normal': normal_data,
    'Gamma': gamma_data,
    'Beta' : beta_data,
    'ChiSquare': chi_square_data,
    'RandomIntegers': random_integers
})

# Save to CSV
df.to_csv('distributions.csv', index=False)

