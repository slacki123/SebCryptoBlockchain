from backend.util.crypto_hash import crypto_hash

HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}


def hex_to_binary(hex_string):
    """
    Function needed to make the difficulty check more precise since checking the leading 0's in a hex value
    is not as precise
    :param hex_string:
    :return:
    """
    binary_string = ''
    for char in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[char]

    return binary_string


def main():
    number = 451
    hex_number = hex(number)[2:]
    print(f'Hex number: {hex_number}')

    binary_number = hex_to_binary(hex_number)

    print(f'Binary number: {binary_number}')

    # convert  binary back to int
    original_number = int(binary_number, 2)
    print(f'Original number: {original_number}')

    hex_to_binary_crypto_hash = hex_to_binary(crypto_hash('test-data'))
    print(f'Hex to binary: {hex_to_binary_crypto_hash}')


if __name__ == '__main__':
    main()
