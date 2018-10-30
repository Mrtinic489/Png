from Byte_parser import parse_bytes


class tIME:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        self.parsed_data['Year'] = parse_bytes(self.parsed_data, [0, 2])[0]
        self.parsed_data['Month'] = self.parsed_data[2]
        self.parsed_data['Day'] = self.parsed_data[3]
        self.parsed_data['Hour'] = self.parsed_data[4]
        self.parsed_data['Minute'] = self.parsed_data[5]
        self.parsed_data['Second'] = self.parsed_data[6]