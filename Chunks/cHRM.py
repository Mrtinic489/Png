from Byte_parser import parse_bytes


class cHRM:

    def __init__(self,byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        from_bytes = parse_bytes(self.byte_data, [0, 4, 8, 12, 16, 20, 24, 28, 32])
        self.parsed_data['White point x'] = from_bytes[0] / 100000
        self.parsed_data['White point y'] = from_bytes[1] / 100000
        self.parsed_data['Red x'] = from_bytes[2] / 100000
        self.parsed_data['Red y'] = from_bytes[3] / 100000
        self.parsed_data['Green x'] = from_bytes[4] / 100000
        self.parsed_data['Green y'] = from_bytes[5] / 100000
        self.parsed_data['Blue x'] = from_bytes[6] / 100000
        self.parsed_data['Blue y'] = from_bytes[7] / 100000