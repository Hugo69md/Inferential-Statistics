import pandas as pd #type: ignore
from utils.data_selection.one_column_case.one_column_selection import one_column_selection
from utils.data_selection.two_columns_case.two_columns_selection import two_columns_selection

def data_selection(df, plotinput):
    if plotinput == 1 or plotinput == 3 :
        col1, col2 = one_column_selection(df)
    else:
        col1, col2 = two_columns_selection(df)

    return col1, col2