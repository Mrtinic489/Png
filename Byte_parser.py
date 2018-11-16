def parse_bytes(byte_list, args, f=None):
    result = []
    if f is None:
        for i in range(len(args) - 1):
            result.append(int.from_bytes(byte_list[args[i]: args[i + 1]], 'big'))
    else:
        for i in range(0, len(args) - 1, 2):
            result.append(int.from_bytes(byte_list[args[i]: args[i + 1]], 'big'))
    return result


def from_bin_to_dec(number):
    result = 0
    for i in range(len(number)):
        result += pow(2, len(number) - i - 1) * int(number[i])
    return result


def from_hex_to_bin(number):
    int_number = int.from_bytes(number, 'big')
    bin_number = bin(int_number).replace('b', '')
    while len(bin_number) > 8:
        bin_number = bin_number[1:]
    while len(bin_number) < 8:
        bin_number = '0' + bin_number
    return bin_number


def from_dec_to_bin(number):
    bin_number = bin(number).replace('b', '')
    while len(bin_number) > 8:
        bin_number = bin_number[1:]
    while len(bin_number) < 8:
        bin_number = '0' + bin_number
    return bin_number