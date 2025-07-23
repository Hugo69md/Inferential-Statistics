import pandas as pd #type: ignore
import numpy as np #type: ignore

def dfmodif(df):
    """-------------------------------APPLY FILTERS---------------------------------------"""
    # Remove rows with NaN values
    #df = df[df['Customer_Age'] == 30]
    #df = df[df['Month'] == 'May']
    #df = df[df['Customer_Gender'] == 'M']
    
    df = df[df['RandomIntegers'] == (44)]
    """-------------------------------END OF APPLYING FILTERS-----------------------------"""

    """========================================================================================================"""

    """-------------------------------ADD / TRANSFORM DATA -------------------------------"""
    #random_numbers = np.random.rand(len(df))

    # Round the numbers to 5 decimal places
    #random_numbers_rounded = np.round(random_numbers, 5)

    # Add the rounded random numbers as a new column
    """df['RandomNumbers'] = random_numbers_rounded
    df['Profitspé'] = df['Profit'] * df['RandomNumbers']
    df["ones"] = df['Profit'] / df['Profit']
    df["ones"].fillna(1, inplace=True)"""

    """-------------------------------END OF ADD / TRANSFORM DATA-------------------------"""

    # Reset the index of the DataFrame 
    df.reset_index(drop=True, inplace=True)
    
    return df