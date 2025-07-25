def caesar_cipher(text, shift, mode='encode'):
    result = ""
    shift = shift % 26
    if mode == 'decode':
        shift = -shift

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

print("Encoded:", caesar_cipher("Hello World", 3))
print("Decoded:", caesar_cipher("Khoor Zruog", 3, 'decode'))