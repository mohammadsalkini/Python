




//* code written by: Mohammad Alsalkini





# to check the validity of the number


def check(credit):

    length = 0
    number = [0 for i in range(16)]
    sum1 = 0
    # put the number in an arrey
    for i in range(1, 17, 1):
        if credit / 10 > 0:
            # length: is the length of the number
            length += 1
            rest = credit % 10
            number[16 - i] = rest
            credit = (credit - rest) / 10

        else:
            number[16 - i] = 0

    # check if the number valid or not
    x = 16 - length
    for m in range(length - 1, x + 1, -2):
        if number[m - 1] * 2 > 9:
            sum1 = sum1 + (number[m - 1] * 2) % 10 + 1

        else:
            sum1 = sum1 + number[m - 1] * 2

        sum1 = sum1 + number[m]

    if sum1 % 10 == 0:
        return True

    return False

# to check the type of the card


def type(credit):
    # AMEX
    if (credit >= 340000000000000 and credit < 350000000000000) or (credit >= 370000000000000 and credit < 380000000000000):
        return 1

    # MASTERCARD
    if credit >= 5100000000000000 and credit < 5600000000000000:
        return 2

    # VISA
    if (credit >= 4000000000000000 and credit < 5000000000000000) or (credit >= 4000000000000 and credit < 5000000000000):
        return 3

    return 0

# to print out the type of the card if it is valid


def print_cardtype(card_type):

    if card_type == 0:
        print(f"INVALID")

    elif card_type == 1:
        print(f"AMEX")

    elif card_type == 2:
        print(f"MASTERCARD")

    elif card_type == 3:
        print(f"VISA")


def main():

    # the user input
    print("Number: ", end="")
    credit = (int)(input())
    credit_type = 0
    credit_type = type(credit)

    if check(credit) == True:
        credit_type = 0

    print_cardtype(credit_type)


if __name__ == "__main__":
    main()