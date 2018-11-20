from Byte_parser import parse_bytes


class tIME:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        self.parsed_data['Year'] = parse_bytes(self.byte_data, [0, 2])[0]
        self.parsed_data['Month'] = self.byte_data[2]
        self.parsed_data['Day'] = self.byte_data[3]
        self.parsed_data['Hour'] = self.byte_data[4]
        self.parsed_data['Minute'] = self.byte_data[5]
        self.parsed_data['Second'] = self.byte_data[6]