class sRGB:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        self.parsed_data['Rendering intent'] = self.byte_data[0]