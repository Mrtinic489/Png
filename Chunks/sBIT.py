class sBIT:

    def __init__(self, ihdr, byte_data):
        self.ihdr = ihdr
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        if self.ihdr.parsed_data['Color info'] == 'Grayscale':
            self.parsed_data['Significant info'] = self.byte_data[0]
        elif self.ihdr.parsed_data['Color info'] == 'RGB' or self.ihdr.parsed_data['Color info'] == 'Индексированные значения':
            self.parsed_data['Significant info red'] = self.byte_data[0]
            self.parsed_data['Significant info green'] = self.byte_data[1]
            self.parsed_data['Significant info blue'] = self.byte_data[2]
        elif self.ihdr.parsed_data['Color info'] == 'Grayscale + alpha channel':
            self.parsed_data['Significant info grayscale'] = self.byte_data[0]
            self.parsed_data['Significant info alpha'] = self.byte_data[1]
        else:
            self.parsed_data['Significant info red'] = self.byte_data[0]
            self.parsed_data['Significant info green'] = self.byte_data[1]
            self.parsed_data['Significant info blue'] = self.byte_data[2]
            self.parsed_data['Significant info alpha'] = self.byte_data[3]