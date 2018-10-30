import zlib


class IDAT:

    def __init__(self, ihdr, byte_data):
        self.ihdr = ihdr
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        result = zlib.decompress(self.byte_data)
        data = ''
        for item in result:
            bin_number = bin(item).replace('b', '')
            while len(bin_number) > 8:
                bin_number = bin_number[1:]
            while len(bin_number) < 8:
                bin_number = '0' + bin_number
            bin_number = bin_number[::-1]
            data.join(bin_number)
            self.parsed_data['data'] = data