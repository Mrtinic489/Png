import zlib
import math
from Utils.Byte_parser import from_dec_to_bin, from_bin_to_dec


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

    def interlace(self, byte_data):
        list_of_positions = [
            [8, 8, 1, 1], [8, 8, 1, 5], [8, 4, 5, 1], [4, 4, 1, 3],
            [4, 2, 3, 1], [2, 2, 1, 2], [2, 1, 2, 1]]

        scanlines_and_pixels_count = []

        for i in range(7):
            scanlines_count = \
                (self.height +
                 list_of_positions[i][0] - list_of_positions[i][2])\
                // list_of_positions[i][0]
            pixels_count = \
                (self.width +
                 list_of_positions[i][1] - list_of_positions[i][3])\
                // list_of_positions[i][1]
            scanlines_and_pixels_count.append(tuple(
                [scanlines_count, pixels_count]))

        bytes_list = [[] for i in range(7)]

        total_index = 0
        for index, item in enumerate(scanlines_and_pixels_count):
            scanline_length = self.find_scanline_length_fro_interlace(item[1])
            for i in range(item[0]):
                byte_str = byte_data[total_index:total_index + scanline_length]
                result_str = ''.join(
                    [from_dec_to_bin(item) for item in byte_str])
                bytes_list[index].append(result_str)
                total_index += scanline_length
        list_of_all_pixels = []
        for index, item in enumerate(bytes_list):
            list_of_all_pixels.append(
                self.decode_interlace(item,
                                      scanlines_and_pixels_count[index][1]))

        result = []
        for j in range(self.height):
            line = []
            for i in range(self.width):
                line.append([])
            result.append(line)

        for index, item in enumerate(list_of_all_pixels):
            for j, line in enumerate(item):
                times_in_line = list_of_positions[index][0]
                times_in_coloum = list_of_positions[index][1]
                first_in_line = list_of_positions[index][2] - 1
                first_in_coloum = list_of_positions[index][3] - 1
                for i, pixel in enumerate(line):
                    result[first_in_line + j *
                           times_in_line][first_in_coloum + i *
                                          times_in_coloum] = pixel

        self.parsed_data['Result of decoding'] = result

    def decode_interlace(self, raw_list_of_pixels, count_of_pixels):
        list_of_pixels = []
        width = math.ceil(
            count_of_pixels * self.return_size_of_pixel() *
            self.bit_depth / 8) + 1
        size = self.return_size_of_pixel()
        for index, line in enumerate(raw_list_of_pixels):
            filter = from_bin_to_dec(line[:8])
            pixel_line = []
            sub_line = []
            for i in range(8, width * 8, self.bit_depth):
                sub_line.append(from_bin_to_dec(line[i:i+self.bit_depth]))
            for i in range(count_of_pixels):
                pixel = []
                for j in range(size):
                    pixel.append(sub_line[i * size + j])
                pixel_line.append(self.parse_to_rgb(pixel))
            pixel_line = self.filter(filter, pixel_line, list_of_pixels, index)
            list_of_pixels.append(pixel_line)
        return list_of_pixels

    def find_scanline_length_fro_interlace(self, pixel_count):
        return math.ceil(
            (pixel_count * self.bit_depth *
             self.return_size_of_pixel() + 8) / 8)

    def analize(self):
        zobj = zlib.decompressobj()
        decompress_bytes = zobj.decompress(self.byte_data)
        if self.interlaced == 'Adam7 interlace':
            self.interlace(decompress_bytes)
            return
        width = self.find_width_in_bytes()
        raw_list_of_pixels = []
        for j in range(self.height):
            line = ''
            try:
                line = ''.join(
                    from_dec_to_bin(decompress_bytes[j * width + i])
                    for i in range(width))
                raw_list_of_pixels.append(line)
            except Exception:
                raw_list_of_pixels.append(line)
        self.parsed_data['Result of decoding']\
            = self.decoding(raw_list_of_pixels)

    def decoding(self, raw_list_of_pixels):
        list_of_pixels = []
        width = self.find_width_in_bytes()
        size = self.return_size_of_pixel()
        try:
            for index, line in enumerate(raw_list_of_pixels):
                filter = from_bin_to_dec(line[:8])
                pixel_line = []
                sub_line = []
                for i in range(8, width * 8, self.bit_depth):
                    sub_line.append(from_bin_to_dec(line[i:i+self.bit_depth]))
                for i in range(self.width):
                    pixel = []
                    for j in range(size):
                        pixel.append(sub_line[i * size + j])
                    pixel_line.append(self.parse_to_rgb(pixel))
                pixel_line = self.filter(
                    filter, pixel_line, list_of_pixels, index)
                list_of_pixels.append(pixel_line)
            return list_of_pixels
        except Exception:
            return list_of_pixels

    def filter_1(self, current):
        result_line = []
        for i in range(len(current)):
            result_pixel = []
            for j in range(len(current[i])):
                if i > 0:
                    result_pixel.append(
                        (current[i][j] + (result_line[i - 1][j])) % 256)
                else:
                    result_pixel.append(current[i][j])
            result_line.append(result_pixel)
        return result_line

    def filter_2(self, current, previous):
        result_line = []
        for i in range(len(current)):
            result_pixel = []
            for j in range(len(current[i])):
                result_pixel.append((current[i][j] + previous[i][j]) % 256)
            result_line.append(result_pixel)
        return result_line

    def filter_3(self, current, previous):
        result_line = []
        if previous is None:
            for i in range(len(current)):
                result_pixel = []
                for j in range(len(current[i])):
                    if i > 0:
                        result_pixel.append(
                            (current[i][j] + math.floor(
                                (result_line[i - 1][j]) / 2)) % 256)
                    else:
                        result_pixel.append(current[i][j])
                result_line.append(result_pixel)
            return result_line
        for i in range(len(current)):
            result_pixel = []
            for j in range(len(current[i])):
                if i > 0:
                    result_pixel.append(
                        (current[i][j] + math.floor(
                            (result_line[i - 1][j] + previous[i][j]) / 2))
                        % 256)
                else:
                    result_pixel.append(
                        (current[i][j] + math.floor(previous[i][j] / 2)) % 256)
            result_line.append(result_pixel)
        return result_line

    def filter_4(self, current, previous):
        result_line = []
        if previous is None:
            for i in range(len(current)):
                result_pixel = []
                for j in range(len(current[i])):
                    if i > 0:
                        result_pixel.append(
                            (current[i][j] +
                             self.paeth_predictor(
                                 result_line[i - 1][j], 0, 0)) % 256)
                    else:
                        result_pixel.append(current[i][j])
                result_line.append(result_pixel)
            return result_line
        for i in range(len(current)):
            result_pixel = []
            for j in range(len(current[i])):
                if i > 0:
                    result_pixel.append(
                        (current[i][j] +
                         self.paeth_predictor(result_line[i - 1][j],
                                              previous[i][j],
                                              previous[i-1][j])) % 256)
                else:
                    result_pixel.append(
                        (current[i][j] + self.paeth_predictor(
                            0, previous[i][j], 0)) % 256)
            result_line.append(result_pixel)
        return result_line

    def paeth_predictor(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            return a
        elif pb <= pc:
            return b
        else:
            return c

    def filter(self, filter_type, current, list_of_pixels, index):
        if filter_type == 0:
            return current

        if filter_type == 1:
            return self.filter_1(current)

        if filter_type == 2:
            if index == 0:
                return current
            else:
                return self.filter_2(current, list_of_pixels[index - 1])

        if filter_type == 3:
            if index == 0:
                return self.filter_3(current, None)
            else:
                return self.filter_3(current, list_of_pixels[index - 1])

        if filter_type == 4:
            if index == 0:
                return self.filter_4(current, None)
            else:
                return self.filter_4(current, list_of_pixels[index - 1])

    def find_width_in_bytes(self):
        color = self.color_type
        bit_depth = self.bit_depth
        if color == 'Grayscale' or color == 'Индексированные значения':
            return math.ceil((self.width * bit_depth) / 8) + 1
        elif color == 'RGB':
            return math.ceil((self.width * bit_depth * 3) / 8) + 1
        elif color == 'RGBA':
            return math.ceil((self.width * bit_depth * 4) / 8) + 1
        else:
            return math.ceil((self.width * bit_depth * 2) / 8) + 1

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
        elif self.color_type == 'Grayscale' or \
                self.color_type == 'Grayscale + alpha channel':
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
        if self.color_type == 'Grayscale' or \
                self.color_type == 'Индексированные значения':
            return 1
        elif self.color_type == 'Grayscale + alpha channel':
            return 2
        elif self.color_type == 'RGB':
            return 3
        else:
            return 4
