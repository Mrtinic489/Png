import zlib


class iTXt:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        list_of_separators = []
        for i in range(len(self.byte_data)):
            if self.byte_data[i] == 0:
                list_of_separators.append(i)
        key_word = self.byte_data[:list_of_separators[0]].decode()
        if self.byte_data[list_of_separators[0] + 1] == 1:
            text = zlib.decompress(
                self.byte_data[list_of_separators[-1] + 1:]).decode()
        else:
            text = self.byte_data[list_of_separators[-1] + 1:].decode()
        self.parsed_data[key_word] = text
