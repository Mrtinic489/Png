import zlib
import json
from Byte_parser import from_dec_to_bin, from_bin_to_dec


class IDAT:

    def __init__(self, ihdr, plte, byte_data):
        self.ihdr = ihdr
        self.plte = plte
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
        print_str = ''
        for i in range(0, len(bin_str), 8):
            print_str += bin_str[i:i + 8] + ' '
        size = self.return_size_of_pixel()
        self.parsed_data['Result of decoding'] = self.decoding(bin_str, size)

    def parse_to_rgb(self, list_of_pixels):
        result = []
        if self.color_type == 'RGB':
            for item in list_of_pixels:
                if self.bit_depth == 16:
                    result.append((item * 255) // 65535)
                else:
                    result.append(item)
        elif self.color_type == 'RGBA':
            for item in list_of_pixels:
                if self.bit_depth == 16:
                    result.append(item * 255 // 65535)
                else:
                    result.append(item)
            t = result[0]
            result[0] = result[3]
            result[3] = t
        elif self.color_type == 'Grayscale' or self.color_type == 'Grayscale + alpha channel':
            if self.bit_depth == 1:
                index = 255
            elif self.bit_depth == 2:
                index = 85
            elif self.bit_depth == 4:
                index = 16
            elif self.bit_depth == 8:
                index = 1
            else:
                index = 255 / 65535
            for i in range(3):
                result.append(int(list_of_pixels[-1] * index))
            if self.color_type != 'Grayscale':
                result.append(int(list_of_pixels[0] * index))
        else:
            item = list_of_pixels[0]
            for i in range(3):
                result.append(self.plte.parsed_data[item][i])
        return result

    def return_size_of_pixel(self):
        if self.color_type == 'Grayscale' or self.color_type == 'Индексированные значения':
            return 1
        elif self.color_type == 'Grayscale + alpha channel':
            return 2
        elif self.color_type == 'RGB':
            return 3
        else:
            return 4

    def reutrn_bpp(self):
        if self.color_type == 'Grayscale':
            if self.bit_depth <= 8:
                return 1
            else:
                return 2
        elif self.color_type == 'RGB':
            if self.bit_depth == 8:
                return 3
            else:
                return 6
        elif self.color_type == 'Индексированные значения':
            return 1
        elif self.color_type == 'Grayscale + alpha channel':
            if self.bit_depth == 8:
                return 2
            else:
                return 4
        elif self.bit_depth == 8:
            return 4
        else:
            return 8

    def decoding(self, data, size):
        result = []
        pointer = 0
        for j in range(self.height):
            row = []
            list_for_filter = []
            filter = from_bin_to_dec(data[pointer:pointer + 8])
            bpp = self.reutrn_bpp()
            pointer += 8
            for i in range(self.width):
                sub_result = []
                for k in range(size):
                    current = from_bin_to_dec(data[pointer:pointer + self.bit_depth])
                    if filter == 1:
                        index = i * size + k - bpp
                        if index < 0:
                            index = 0
                        if len(list_for_filter) != 0:
                            current = (current + list_for_filter[index]) % 256
                    list_for_filter.append(current)
                    pointer += self.bit_depth
                    sub_result.append(current)
                row.append(self.parse_to_rgb(sub_result))
            if pointer % 8 != 0:
                pointer += 8 - pointer % 8
            result.append(row)
        return result
