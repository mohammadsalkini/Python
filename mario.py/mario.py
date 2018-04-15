




//* code written by: Mohammad Alsalkini




from cs50 import get_int
# the input of the user
height = get_int("Height: ")

while height:

    # checking the number
    if height > 0 and height < 24:

        # print the spaces
        for line in range(height):

            for spaces in range(height - line - 1):

                print(f" ", end="")

            # reight side
            for hashes in range(line + 1):

                print(f"#", end="")

            print(f"  ", end="")

            # left side
            for hashes2 in range(line + 1):

                print(f"#", end="")

            print()

        break

    # invalid number
    else:
        height = get_int("Height: ")