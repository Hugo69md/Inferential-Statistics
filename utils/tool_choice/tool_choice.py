def tool_choice():
    print("What type of tool would you like to use among those ? \n1 sample T-test (press 1), \n2 samples T-test (press 2), \n1 sample non_param test (press 3), \n2 samples non_param test (press 4).")
    while True:
        try:
            toolinput = int(input("Enter your choice: "))
            if not toolinput in range(1,5): # Change if need to add more tools
                raise ValueError
            return toolinput
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")