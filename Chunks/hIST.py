from Utils.Byte_parser import parse_bytes


class hIST:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        for i in range(0, len(self.byte_data), 2):
            self.parsed_data['Hist info ' + str(i)] =\
                parse_bytes(self.parsed_data, [i, i+2], False)[0]
