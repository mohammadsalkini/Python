from cs50 import get_int
class Caesar:
    def encrypt_character(self, character, key):
        if character.isalpha():
            # checking if the input is an alphapet
            if character.isupper():
                cipherletter = chr(((ord(character) - 65 + key) % 26) + 65)
                return cipherletter
            # checking if the input is capital letter
            else:
                cipherletter = chr(((ord(character) - 97 + key) % 26) + 97)
                return cipherletter
        # The input is not an alphapet
        return character

    def get_positive_int(self, number):
        while number < 0:
            number = get_int("a positive number please: ")
        return number

    def decrypt_character(self, character, key):
        if character.isalpha():
            # checking if the input is an alphapet
            if character.isupper():
                letter = chr(((ord(character) - 65 - key) % 26) + 65)
                return letter
            # checking if the input is capital letter
            else:
                letter = chr(((ord(character) - 97 - key) % 26) + 97)
                return letter
        # The input is not an alphapet
        return character