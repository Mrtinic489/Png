from Utils.Byte_parser import parse_bytes


class sPLT:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        index = 0
        for i in range(len(self.byte_data)):
            if self.byte_data[i] == 0:
                index = i
                break
        sample_depth = self.byte_data[index + 1]
        if sample_depth == 8:
            self.parsed_data['sPLT info red'] = self.byte_data[index + 2]
            self.parsed_data['sPLT info green'] = self.byte_data[index + 3]
            self.parsed_data['sPLT info blue'] = self.byte_data[index + 4]
            self.parsed_data['sPLT info alpha'] = self.byte_data[index + 5]
            self.parsed_data['sPLT info frecuency'] = \
                parse_bytes(self.byte_data, [index + 6, index + 8], False)[0]
        else:
            from_bytes = parse_bytes(
                self.byte_data, [index + i for i in [2, 4, 5, 6, 7, 8, 9, 10]],
                True)
            self.parsed_data['sPLT info red'] = from_bytes[0]
            self.parsed_data['sPLT info green'] = from_bytes[1]
            self.parsed_data['sPLT info blue'] = from_bytes[2]
            self.parsed_data['sPLT info alpha'] = from_bytes[3]
