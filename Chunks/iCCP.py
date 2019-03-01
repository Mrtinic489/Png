import zlib


class iCCP:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        index = 0
        for i in range(len(self.byte_data)):
            if self.byte_data[i] == 0:
                index = i
                break
        profile_name = self.byte_data[:index].decode()
        profile = zlib.decompress(self.byte_data[index + 2:])
        self.parsed_data[profile_name] = profile
