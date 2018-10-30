class tRNS:

    def __init__(self, ihdr, byte_data):
        self.ihdr = ihdr
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        if self.ihdr.parsed_data['Color info'] == 'Индексированные значения':
            for i in range(len(self.byte_data)):
                self.parsed_data['Alpha for index ' + str(i)] = self.byte_data[i]
        elif self.ihdr.parsed_data['Color info'] == 'Grayscale':
            self.parsed_data['Gray tRNS'] = int.from_bytes(self.byte_data[:2], 'big')
        elif self.ihdr.parsed_data['Color info'] == 'RGB':
            self.parsed_data['RGB tRNS'] = tuple([self.byte_data[0], self.byte_data[1], self.byte_data[2]])