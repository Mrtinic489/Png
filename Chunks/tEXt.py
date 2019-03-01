class tEXt:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        result_str = self.byte_data.decode()
        result_str = result_str.split('\x00')
        self.parsed_data[result_str[0]] = result_str[1]
