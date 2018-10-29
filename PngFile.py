from Chunk import Chunk
import zlib
import sys


class PngFile:

    def __init__(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.file = f.read()
                self.header = self.file[:8]
                if self.header[0] != 137 or self.header[1:4].decode('ascii') != 'PNG':
                    print('Not png')
                    sys.exit()
        except Exception:
            print('Fie not found')
            sys.exit()
        self.list_of_raw_chunks = []
        self.find_chunks()
        self.decoded_chunks = []
        self.IHDRchunk = Chunk(self.list_of_raw_chunks[0])
        self.IHDRanalize(self.IHDRchunk)
        self.decoded_chunks.append(self.IHDRchunk)
        self.analize_chunks()

    def analize_chunks(self):
        for i in range(1, len(self.list_of_raw_chunks)):
            chunk = Chunk(self.list_of_raw_chunks[i])
            if chunk.type == 'iTXt':
                self.iTXtanalize(chunk)
            elif chunk.type == 'tEXt':
                self.tEXtanalize(chunk)
            elif chunk.type == 'zTXt':
                self.zTXtanalize(chunk)
            elif chunk.type == 'cHRM':
                self.cHRManalize(chunk)
            elif chunk.type == 'gAMA':
                self.gAMAanalize(chunk)
            elif chunk.type == 'iCCP':
                self.iCCPanalize(chunk)
            elif chunk.type == 'sRGB':
                self.sRGBanalize(chunk)
            elif chunk.type == 'bKGD':
                self.bKGDanalize(self.IHDRchunk, chunk)
            elif chunk.type == 'tRNS':
                self.tRNSanalize(self.IHDRchunk, chunk)
            elif chunk.type == 'pHYs':
                self.pHYsanalize(chunk)
            elif chunk.type == 'tIME':
                self.tIMEamalize(chunk)
            elif chunk.type == 'PLTE':
                self.PLTEanalize(chunk)
            elif chunk.type == 'sBIT':
                self.sBITanalize(self.IHDRchunk, chunk)
            elif chunk.type == 'hIST':
                self.hISTanalize(chunk)
            elif chunk.type == 'sPLT':
                self.sPLTanalize(chunk)
            elif chunk.type == 'IEND':
                self.IENDanalize(chunk)
            self.decoded_chunks.append(chunk)


    def print_info(self):
        for item in self.decoded_chunks:
            if len(item.data_dict.items()) != 0:
                print(item.data_dict.items())

    def find_chunks(self):
        index = 8
        while(index < len(self.file)):
            length = int.from_bytes(self.file[index:index + 4], 'big')
            self.list_of_raw_chunks.append(self.file[index:index + 12 + length])
            index += 12 + length

    def from_bytes(self, byte_list, args, f = None):
        result = []
        if f == None:
            for i in range(len(args) - 1):
                result.append(int.from_bytes(byte_list[args[i]: args[i + 1]], 'big'))
        else:
            for i in range(0, len(args) - 1, 2):
                result.append(int.from_bytes(byte_list[args[i]: args[i + 1]], 'big'))
        return result

    def IHDRanalize(self, chunk):
        from_bytes = self.from_bytes(chunk.raw_chunk_data, [0, 4, 8])
        chunk.data_dict['Width'] = from_bytes[0]
        chunk.data_dict['Height'] = from_bytes[1]
        chunk.data_dict['Bit depth'] = chunk.raw_chunk_data[8]
        color_info = chunk.raw_chunk_data[9]
        if color_info == 0:
            chunk.data_dict['Color info'] = 'Grayscale'
        elif color_info == 2:
            chunk.data_dict['Color info'] = 'RGB'
        elif color_info == 3:
            chunk.data_dict['Color info'] = 'Индексированные значения'
        elif color_info == 4:
            chunk.data_dict['Color info'] = 'Grayscale + alpha channel'
        elif color_info == 6:
            chunk.data_dict['Color info'] = 'RGBA'
        if chunk.raw_chunk_data[10] == 0:
            chunk.data_dict['Compress method'] = 'Deflate compress method'
        if chunk.raw_chunk_data[11] == 0:
            chunk.data_dict['Filter method'] = 'Correct'
        if chunk.raw_chunk_data[12] == 0:
            chunk.data_dict['Interlace info'] = 'No interlace'
        else:
            chunk.data_dict['Interlace info'] = 'Adam7 interlace'

    def IDATanalize(self, ihdr_chunk, chunk):
        result = zlib.decompress(chunk.raw_chunk_data)
        data = ''
        for item in result:
            bin_number = bin(item).replace('b', '')
            while len(bin_number) > 8:
                bin_number = bin_number[1:]
            while len(bin_number) < 8:
                bin_number = '0' + bin_number
            bin_number = bin_number[::-1]
            data.join(bin_number)
            chunk.data_dict['data'] = data

    def PLTEanalize(self, chunk):
        for i in range(0, len(chunk.raw_chunk_data), 3):
            chunk.data_dict[i // 3] =\
                tuple([chunk.raw_chunk_data[i], chunk.raw_chunk_data[i + 1], chunk.raw_chunk_data[i + 2]])

    def bKGDanalize(self, ihdr_chunk, chunk):
        from_bytes = self.from_bytes(chunk.raw_chunk_data, [0, 2, 4, 6])
        if ihdr_chunk.data_dict['Color info'] == 'Индексированные значения':
            chunk.data_dict['Pallete index'] = chunk.raw_chunk_data[0]
        elif ihdr_chunk.data_dict['Color info'] == 'Grayscale' or ihdr_chunk.data_dict['Color info'] == 'Grayscale + alpha channel':
            chunk.data_dict['Gray'] = from_bytes[0]
        else:
            chunk.data_dict['Red'] = from_bytes[0]
            chunk.data_dict['Green'] = from_bytes[1]
            chunk.data_dict['Blue'] = from_bytes[2]

    def cHRManalize(self, chunk):
        from_bytes = self.from_bytes(chunk.raw_chunk_data, [0, 4, 8, 12, 16, 20, 24, 28, 32])
        chunk.data_dict['White point x'] = from_bytes[0] / 100000
        chunk.data_dict['White point y'] = from_bytes[1] / 100000
        chunk.data_dict['Red x'] = from_bytes[2] / 100000
        chunk.data_dict['Red y'] = from_bytes[3] / 100000
        chunk.data_dict['Green x'] = from_bytes[4] / 100000
        chunk.data_dict['Green y'] = from_bytes[5] / 100000
        chunk.data_dict['Blue x'] = from_bytes[6] / 100000
        chunk.data_dict['Blue y'] = from_bytes[7] / 100000

    def gAMAanalize(self, chunk):
        chunk.data_dict['Gamma value'] = self.from_bytes(chunk.raw_chunk_data, [0, 4])[0] / 100000

    def hISTanalize(self, chunk):
        for i in range(0, len(chunk.raw_chunk_data), 2):
            chunk.data_dict['Hist info ' + str(i)] = int.from_bytes(chunk.raw_chunk_data[i:i+2], 'big')

    def sBITanalize(self, ihdr_chunk, chunk):
        if ihdr_chunk.data_dict['Color info'] == 'Grayscale':
            chunk.data_dict['Significant info'] = chunk.raw_chunk_data[0]
        elif ihdr_chunk.data_dict['Color info'] == 'RGB' or ihdr_chunk.data_dict['Color info'] == 'Индексированные значения':
            chunk.data_dict['Significant info red'] = chunk.raw_chunk_data[0]
            chunk.data_dict['Significant info green'] = chunk.raw_chunk_data[1]
            chunk.data_dict['Significant info blue'] = chunk.raw_chunk_data[2]
        elif ihdr_chunk.data_dict['Color info'] == 'Grayscale + alpha channel':
            chunk.data_dict['Significant info grayscale'] = chunk.raw_chunk_data[0]
            chunk.data_dict['Significant info alpha'] = chunk.raw_chunk_data[1]
        else:
            chunk.data_dict['Significant info red'] = chunk.raw_chunk_data[0]
            chunk.data_dict['Significant info green'] = chunk.raw_chunk_data[1]
            chunk.data_dict['Significant info blue'] = chunk.raw_chunk_data[2]
            chunk.data_dict['Significant info alpha'] = chunk.raw_chunk_data[3]


    def sRGBanalize(self, chunk):
        chunk.data_dict['Rendering intent'] = chunk.raw_chunk_data[0]

    def pHYsanalize(self, chunk):
        from_bytes = self.from_bytes(chunk.raw_chunk_data, [0, 4, 8])
        chunk.data_dict['Unit specifire'] = chunk.raw_chunk_data[8]
        if chunk.data_dict['Unit specifire'] == 1:
            chunk.data_dict['Pixels per meter, X'] = from_bytes[0]
            chunk.data_dict['Pixels per meter, Y'] = from_bytes[1]
        else:
            chunk.data_dict['Pixels per unknow unit, X'] = from_bytes[0]
            chunk.data_dict['Pixels per unknow unit, Y'] = from_bytes[1]

    def iCCPanalize(self, chunk):
        index = 0
        for i in range(len(chunk.raw_chunk_data)):
            if chunk.raw_chunk_data[i] == 0:
                index = i
                break
        profile_name = chunk.raw_chunk_data[:index].decode()
        profile = zlib.decompress(chunk.raw_chunk_data[index + 2:])
        chunk.data_dict[profile_name] = profile

    def iTXtanalize(self, chunk):
        list_of_separators = []
        for i in range(len(chunk.raw_chunk_data)):
            if chunk.raw_chunk_data[i] == 0:
                list_of_separators.append(i)
        key_word = chunk.raw_chunk_data[:list_of_separators[0]].decode()
        text = ""
        if chunk.raw_chunk_data[list_of_separators[0] + 1] == 1:
            text = zlib.decompress(chunk.raw_chunk_data[list_of_separators[-1] + 1:]).decode()
        else:
            text = chunk.raw_chunk_data[list_of_separators[-1] + 1:].decode()
        chunk.data_dict[key_word] = text

    def zTXtanalize(self, chunk):
        index = 0
        for i in range(len(chunk.raw_chunk_data)):
            if chunk.raw_chunk_data[i] == 0:
                index = i
                break
        key_word = chunk.raw_chunk_data[:index].decode()
        result = zlib.decompress(chunk.raw_chunk_data[index + 2:]).decode()
        chunk.data_dict[key_word] = result

    def tEXtanalize(self, chunk):
        result_str = chunk.raw_chunk_data.decode()
        result_str = result_str.split('\x00')
        chunk.data_dict[result_str[0]] = result_str[1]

    def tIMEamalize(self, chunk):
        chunk.data_dict['Year'] = self.from_bytes(chunk.raw_chunk_data, [0, 2])[0]
        chunk.data_dict['Month'] = chunk.raw_chunk_data[2]
        chunk.data_dict['Day'] = chunk.raw_chunk_data[3]
        chunk.data_dict['Hour'] = chunk.raw_chunk_data[4]
        chunk.data_dict['Minute'] = chunk.raw_chunk_data[5]
        chunk.data_dict['Second'] = chunk.raw_chunk_data[6]


    def tRNSanalize(self, ihdr_chunk, chunk):
        if ihdr_chunk.data_dict['Color info'] == 'Индексированные значения':
            for i in range(len(chunk.raw_chunk_data)):
                chunk.data_dict['Alpha for index ' + str(i)] = chunk.raw_chunk_data[i]
        elif ihdr_chunk.data_dict['Color info'] == 'Grayscale':
            chunk.data_dict['Gray'] = int.from_bytes(chunk.raw_chunk_data[:2], 'big')
        elif ihdr_chunk.data_dict['Color info'] == 'RGB':
            chunk.data_dict['RGB'] = tuple([chunk.raw_chunk_data[0], chunk.raw_chunk_data[1], chunk.raw_chunk_data[2]])

    def sPLTanalize(self, chunk):
        index = 0
        for i in range(len(chunk.raw_chunk_data)):
            if chunk.raw_chunk_data[i] == 0:
                index = i
                break
        sample_depth = chunk.raw_chunk_data[index + 1]
        if sample_depth == 8:
            chunk.data_dict['sPLT info red'] = chunk.raw_chunk_data[index + 2]
            chunk.data_dict['sPLT info green'] = chunk.raw_chunk_data[index + 3]
            chunk.data_dict['sPLT info blue'] = chunk.raw_chunk_data[index + 4]
            chunk.data_dict['sPLT info alpha'] = chunk.raw_chunk_data[index + 5]
            chunk.data_dict['sPLT info freuency'] = self.from_bytes(chunk.raw_chunk_data, [index + 6, index + 8])[0]
        else:
            from_bytes = self.from_bytes(chunk.raw_chunk_data, [index + i for i in[2, 4, 5, 6, 7, 8, 9, 10]], True)
            chunk.data_dict['sPLT info red'] = from_bytes[0]
            chunk.data_dict['sPLT info green'] = from_bytes[1]
            chunk.data_dict['sPLT info blue'] = from_bytes[2]
            chunk.data_dict['sPLT info alpha'] = from_bytes[3]

    def IENDanalize(self, chunk):
        if chunk.type == 'IEND':
            chunk.data_dict['State'] = 'Correct'
        else:
            chunk.data_dict['State'] = 'Uncorrect'