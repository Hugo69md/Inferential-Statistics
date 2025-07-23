import sys
import pandas as pd #type: ignore
from utils.data_selection.one_column_case.indexcolumn import indexcolumn

def one_column_selection(df):
    try: 
        collist = indexcolumn()
        col1 = df.columns[collist[0]]
        col2 = None  # No second column for single column selection 
    except IndexError:
        print("Invalid input. Please enter correct column indexes.")
                
    return col1, col2