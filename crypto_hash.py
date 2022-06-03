import hashlib
import json


def stringify(data):
    return json.dumps(data)


def crypto_hash(*args):
    """
    return sha256 hash of the given arguments. If even one character is different in data, the entire hash will change.
    :param args: the input data arguments
    :return: hashed data
    """
    stringified_args = map(lambda data: json.dumps(data), args)  # convert to string
    stringified_sorted_args = sorted(stringified_args)
    joined_data = ''.join(stringified_sorted_args)
    encoded_data = joined_data.encode('utf-8')  # encode to utf8
    return hashlib.sha256(encoded_data).hexdigest()


def main():
    print(f"crypto_hash([1], 'two', 3): {crypto_hash([1], 'two', 3)}")
    print(f"crypto_hash([1], 3, 'two'): {crypto_hash([1], 3, 'two')}")


if __name__ == '__main__':
    main()

