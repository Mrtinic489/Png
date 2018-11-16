import zlib
import json
from Byte_parser import from_dec_to_bin, from_bin_to_dec


class IDAT:

    def __init__(self, ihdr, byte_data):
        self.ihdr = ihdr
        self.height = ihdr.parsed_data['Height']
        self.width = ihdr.parsed_data['Width']
        self.color_type = ihdr.parsed_data['Color info']
        self.bit_depth = ihdr.parsed_data['Bit depth']
        self.interlaced = ihdr.parsed_data['Interlace info']
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        decompress_bytes = zlib.decompress(self.byte_data)
        bin_str = ''
        for item in decompress_bytes:
            bin_str += from_dec_to_bin(item)
        if self.color_type == 'Индексированные значения' or self.color_type == 'Grayscale':
            self.parsed_data['Result of decoding'] = self.decoding_0_and_2_type(bin_str, self.interlaced)
        else:
            size = self.return_size_of_pixel()
            self.parsed_data['Result of decoding'] = self.decoding_1_3_4_types(bin_str, size)

    def return_size_of_pixel(self):
        if self.color_type == 'RGB':
            return 3
        elif self.color_type == 'Grayscale + alpha channel':
            return 2
        else:
            return 4

    def fixed_haffman_decoding(self, data):
        haffman_dict = dict()
        with open('fixed_haffman_dict', 'r') as f:
            haffman_dict = json.loads(f.read())
        pass

    def dynamic_haffman_decoding(self, data):
        pass

    def decoding_1_3_4_types(self, data, size):
        result = []
        pointer = 0
        for j in range(self.height):
            row = []
            pointer += 8
            for i in range(self.width):
                sub_result = []
                for k in range(size):
                    current = from_bin_to_dec(data[pointer:pointer + self.bit_depth])
                    pointer += self.bit_depth
                    sub_result.append(current)
                row.append(sub_result)
            pointer += 8 - pointer % 8
            result.append(row)
        return result

    def decoding_0_and_2_type(self, data, interlaced):
        result = []
        pointer = 0
        for j in range(self.height):
            row = []
            pointer += 8
            for i in range(self.width):
                current = from_bin_to_dec(data[pointer:pointer+self.bit_depth])
                pointer += self.bit_depth
                row.append(current)
            pointer += 8 - pointer % 8
            result.append(row)
        return result
