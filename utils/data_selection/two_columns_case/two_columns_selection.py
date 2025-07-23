import sys
import pandas as pd #type: ignore
from utils.data_selection.two_columns_case.indexcolumns import indexcolumns

def two_columns_selection(df):
    try: 
        collist = indexcolumns()
        col1 = df.columns[collist[0]]
        col2 = df.columns[collist[1]]
    except IndexError:
        print("Invalid input. Please enter correct column indexes.")
                
    return col1, col2