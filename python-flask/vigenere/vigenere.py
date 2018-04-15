from caesar import Caesar
class Vigenere(Caesar):
    # vigenere's cipher
    def cipher_vigenere(self,plaintext, key):
        keylength = len(key)
        key_counter = 0
        cipher_text = []
        # applying cipher_vigenere
        for character in plaintext:
            shift = 0
            if key_counter == keylength:
                key_counter = 0
            shift = ord(key[key_counter].lower()) - 97

            cipher_text.append(self.encrypt_character(character, shift))
            key_counter += 1
        return "".join(cipher_text)

    def decrypt_vigenere(self,plaintext, key):
        keylength = len(key)
        key_counter = 0
        cipher_text = []
        # applying cipher_vigenere
        for character in plaintext:
            shift = 0
            if key_counter == keylength:
                key_counter = 0
            shift = ord(key[key_counter].lower()) - 97

            cipher_text.append(self.decrypt_character(character, shift))
            key_counter += 1
        return "".join(cipher_text)