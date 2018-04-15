




//* code written by: Mohammad Alsalkini




from cs50 import get_string
from cs50 import get_int
import sys


# accepting a non-negative integer


def get_positive_int(number):
    while number < 0:
        number = get_int("a positive number please: ")
    return number


# applying caesar's cipher

def cipher_caesar(plaintext, key):
    cipher_text = []
    print(f"ciphertext: ", end="")
    for character in plaintext:
        if character.isalpha():
            # checking if the input is an alphapet
            if character.isupper():
                cipherletter = chr(((ord(character) - 65 + key) % 26) + 65)
                cipher_text.append(cipherletter)
            # checking if the input is capital letter
            else:
                cipherletter = chr(((ord(character) - 97 + key) % 26) + 97)
                cipher_text.append(cipherletter)
        # The input is not an alphapet
        else:
            cipher_text.append(character)
    print("".join(cipher_text))


def main():

    # accepting a single command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: ./caesar k")
        exit(1)

    key = int(sys.argv[1])
    key = get_positive_int(key)
    # asking for an input
    plaintext = get_string("plaintext: ")
    cipher_caesar(plaintext, key)


if __name__ == "__main__":
    main()