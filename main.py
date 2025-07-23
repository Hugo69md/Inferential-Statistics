from utils.analysis.analysis import analysis
from utils.tool_choice.tool_choice import tool_choice
from utils.tools.tools_direction import tools_direction
from utils.data_selection.data_selection import data_selection
#from utils.hypotesis_testing.hypothesis_testing import hypothesis_testing
import sys

def main():
    print("Welcome to the inferential statistics Tool!")

    df = analysis()
   
    tool_selection = tool_choice()

    col1, col2 = data_selection(df, tool_selection)
    
    tools_direction(df, tool_selection, col1, col2)


if __name__ == "__main__":
    main()