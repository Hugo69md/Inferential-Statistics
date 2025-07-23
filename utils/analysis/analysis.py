import pandas as pd #type: ignore
from utils.filtering.dfmodif import dfmodif #type: ignore

def analysis():

    dfnew = pd.read_csv('distributions.csv')

    #call the modification function to modify the dataframe
    df = dfmodif(dfnew)

    #displays info about df
    print(df.head())
    print("Here are some statistics about the dataset:")
    print(df.describe())
    print("Here are some infos about the dataset:")
    print(df.info())

    return df