from Byte_parser import parse_bytes


class bKGD:

    def __init__(self, ihdr, byte_data):
        self.ihdr = ihdr
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        from_bytes = parse_bytes(self.byte_data, [0, 2, 4, 6])
        if self.ihdr.parsed_data['Color info'] == 'Индексированные значения':
            self.parsed_data['Pallete index'] = self.byte_data[0]
        elif self.ihdr.parsed_data['Color info'] == 'Grayscale' or \
                self.ihdr.parsed_data['Color info'] == 'Grayscale + alpha channel':
            self.parsed_data['Gray bKGD'] = from_bytes[0]
        else:
            self.parsed_data['Red bKGD'] = from_bytes[0]
            self.parsed_data['Green bKGD'] = from_bytes[1]
            self.parsed_data['Blue bKGD'] = from_bytes[2]