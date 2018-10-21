#!/usr/bin/env python3
from Chunk import Chunk
import zlib

class PngFile:

    def __init__(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.file = f.read()
                self.header = self.file[:8]
                if self.header[0] != 137 or self.header[1:4].decode('ascii') != 'PNG':
                    print('Not png')
                    exit(-1)
        except Exception:
            print('Fie not found')
            exit(-1)
        self.list_of_raw_chunks = []
        self.find_chunks()
        self.IHDRchunk = Chunk(self.list_of_raw_chunks[0])
        self.IHDRanalize(self.IHDRchunk)
        self.IDATchunks = []
        for item in self.list_of_raw_chunks:
            chunk = Chunk(item)
            if chunk.type == 'IDAT':
                self.IDATanalize(chunk)
                self.IDATchunks.append(chunk)
        self.IENDchunk = Chunk(self.list_of_raw_chunks[-1])
        self.IENDanalize(self.IENDchunk)
        self.print_info()

    def print_info(self):
        for pair in self.IHDRchunk.data_dict.items():
            print(pair)
        for item in self.IDATchunks:
            for pair in item.data_dict.items():
                print(pair)
        print(self.IENDchunk.data_dict.items())

    def find_chunks(self):
        index = 8
        while(index < len(self.file)):
            length = int.from_bytes(self.file[index:index + 4], 'big')
            self.list_of_raw_chunks.append(self.file[index:index + 12 + length])
            index += 12 + length

    def IHDRanalize(self, chunk):
        chunk.data_dict['Width'] = int.from_bytes(chunk.raw_chunk_data[:4], 'big')
        chunk.data_dict['Height'] = int.from_bytes(chunk.raw_chunk_data[4:8], 'big')
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

    def IDATanalize(self, chunk):
        result = zlib.decompress(chunk.raw_chunk_data)
        chunk.data_dict['len'] = len(result)

    def PLTEanalize(self, chunk):
        for i in range(0, len(chunk.raw_chunk_data), 3):
            chunk.data_dict[i // 3] =\
                tuple([chunk.raw_chunk_data[i], chunk.raw_chunk_data[i + 1], chunk.raw_chunk_data[i + 2]])

    def bKGDanalize(self, chunk):
        pass

    def cHRManalize(self, chunk):
        chunk.data_dict['White point x'] = int.from_bytes(chunk.raw_chunk_data[:4], 'big') / 100000
        chunk.data_dict['White point y'] = int.from_bytes(chunk.raw_chunk_data[4:8], 'big') / 100000
        chunk.data_dict['Red x'] = int.from_bytes(chunk.raw_chunk_data[8:12], 'big') / 100000
        chunk.data_dict['Red y'] = int.from_bytes(chunk.raw_chunk_data[12:16], 'big') / 100000
        chunk.data_dict['Green x'] = int.from_bytes(chunk.raw_chunk_data[16:20], 'big') / 100000
        chunk.data_dict['Green y'] = int.from_bytes(chunk.raw_chunk_data[20:24], 'big') / 100000
        chunk.data_dict['Blue x'] = int.from_bytes(chunk.raw_chunk_data[24:28], 'big') / 100000
        chunk.data_dict['Blue y'] = int.from_bytes(chunk.raw_chunk_data[28:32], 'big') / 100000

    def gAMAanalize(self, chunk):
        chunk.data_dict['Gama value'] = int.from_bytes(chunk.raw_chunk_data[:4], 'big') / 100000

    def hISTanalize(self, chunk):
        pass

    def sRGBanalize(self, chunk):
        chunk.data_dict['Rendering intent'] = chunk.raw_chunk_data[0]

    def pHYsanalize(self, chunk):
        pass

    def sBITanalize(self, chunk):
        pass

    def iCCPanalize(self, chunk):
        pass

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
        pass

    def tRNSanalize(self, ihdr_chunk, chunk):
        if ihdr_chunk.data_dict['Color info'] == 'Индексированные значения':
            for i in range(len(chunk.raw_chunk_data)):
                chunk.data_dict['Alpha for index ' + str(i)] = chunk.raw_chunk_data[i]
        elif ihdr_chunk.data_dict['Color info'] == 'Grayscale':
            chunk.data_dict['Gray'] = int.from_bytes(chunk.raw_chunk_data[:2], 'big')
        elif ihdr_chunk.data_dict['Color info'] == 'RGB':
            chunk.data_dict['RGB'] = tuple([chunk.raw_chunk_data[0], chunk.raw_chunk_data[1], chunk.raw_chunk_data[2]])

    def IENDanalize(self, chunk):
        if chunk.type == 'IEND':
            chunk.data_dict['State'] = 'Correct'
        else:
            chunk.data_dict['State'] = 'Uncorrect'