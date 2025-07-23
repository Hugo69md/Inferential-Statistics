def indexcolumn():
    while True:
        try:
            col1 = int(input("Enter the column you would like to plot: "))
            collist = [col1]
            break
        except ValueError:
            print("Invalid input. Please enter correct column names.")
    return collist