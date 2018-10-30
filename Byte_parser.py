def parse_bytes(byte_list, args, f=None):
    result = []
    if f is None:
        for i in range(len(args) - 1):
            result.append(int.from_bytes(byte_list[args[i]: args[i + 1]], 'big'))
    else:
        for i in range(0, len(args) - 1, 2):
            result.append(int.from_bytes(byte_list[args[i]: args[i + 1]], 'big'))
    return result
