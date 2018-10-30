from Byte_parser import parse_bytes


class pHYs:

    def __init__(self,byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        from_bytes = parse_bytes(self.byte_data, [0, 4, 8])
        self.parsed_data['Unit specifire'] = self.byte_data[8]
        if self.parsed_data['Unit specifire'] == 1:
            self.parsed_data['Pixels per meter, X'] = from_bytes[0]
            self.parsed_data['Pixels per meter, Y'] = from_bytes[1]
        else:
            self.parsed_data['Pixels per unknow unit, X'] = from_bytes[0]
            self.parsed_data['Pixels per unknow unit, Y'] = from_bytes[1]