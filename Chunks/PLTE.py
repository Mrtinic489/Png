class PLTE:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        for i in range(0, len(self.byte_data), 3):
            self.parsed_data[i // 3] =\
                tuple([self.byte_data[i], self.byte_data[i + 1], self.byte_data[i + 2]])
