from Utils.Byte_parser import parse_bytes


class gAMA:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        self.parsed_data['Gamma value'] = parse_bytes(
            self.byte_data, [0, 4], False)[0] / 100000
