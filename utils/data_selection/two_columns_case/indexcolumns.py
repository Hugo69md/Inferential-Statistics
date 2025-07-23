def indexcolumns():
    while True:
        try:
            col1 = int(input("Enter the first column you would like to plot (this will be X axis): "))
            col2 = int(input("Enter the second column you would like to plot (this will be Y axis): "))
            collist = [col1, col2]
            break
        except ValueError:
            print("Invalid input. Please enter correct column names.")
    return collist