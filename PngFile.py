from Chunk import Chunk
from Byte_parser import parse_bytes
from Chunks.IHDR import IHDR
from Chunks.PLTE import PLTE
from Chunks.iTXt import iTXt
from Chunks.tEXt import tEXt
from Chunks.zTXt import zTXt
from Chunks.cHRM import cHRM
from Chunks.gAMA import gAMA
from Chunks.iCCP import iCCP
from Chunks.sRGB import sRGB
from Chunks.bKGD import bKGD
from Chunks.tRNS import tRNS
from Chunks.pHYs import pHYs
from Chunks.tIME import tIME
from Chunks.sBIT import sBIT
from Chunks.hIST import hIST
from Chunks.sPLT import sPLT
from Chunks.IEND import IEND
from Chunks.IDAT import IDAT
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
        self.list_of_chunks = []
        self.find_chunks()
        self.chunks_dict = dict()
        self.fill_in_dict()

    def find_chunks(self):
        index = 8
        while(index < len(self.file)):
            length = parse_bytes(self.file, [index, index + 4])[0]
            self.list_of_chunks.append(Chunk(self.file[index:index + 12 + length]))
            index += 12 + length

    def fill_in_dict(self):
        for chunk in self.list_of_chunks:
            if chunk.type not in self.chunks_dict.keys():
                self.chunks_dict[chunk.type] = []
            self.chunks_dict[chunk.type].append(self.parse_type(chunk))

    def parse_type(self, chunk):
        if chunk.type == 'IHDR':
            return IHDR(chunk.raw_chunk_data)
        elif chunk.type == 'PLTE':
            return PLTE(chunk.raw_chunk_data)
        elif chunk.type == 'IDAT':
            if 'PLTE' in self.chunks_dict.keys():
                return IDAT(self.chunks_dict['IHDR'][0],self.chunks_dict['PLTE'][0], chunk.raw_chunk_data)
            else:
                return IDAT(self.chunks_dict['IHDR'][0], None, chunk.raw_chunk_data)
        elif chunk.type == 'iTXt':
            return iTXt(chunk.raw_chunk_data)
        elif chunk.type == 'tEXt':
            return tEXt(chunk.raw_chunk_data)
        elif chunk.type == 'zTXt':
            return zTXt(chunk.raw_chunk_data)
        elif chunk.type == 'cHRM':
            return cHRM(chunk.raw_chunk_data)
        elif chunk.type == 'gAMA':
            return gAMA(chunk.raw_chunk_data)
        elif chunk.type == 'iCCP':
            return iCCP(chunk.raw_chunk_data)
        elif chunk.type == 'sRGB':
            return sRGB(chunk.raw_chunk_data)
        elif chunk.type == 'bKGD':
            return bKGD(self.chunks_dict['IHDR'][0], chunk.raw_chunk_data)
        elif chunk.type == 'tRNS':
            return tRNS(self.chunks_dict['IHDR'][0], chunk.raw_chunk_data)
        elif chunk.type == 'pHYs':
            return pHYs(chunk.raw_chunk_data)
        elif chunk.type == 'tIME':
            return tIME(chunk.raw_chunk_data)
        elif chunk.type == 'sBIT':
            return sBIT(self.chunks_dict['IHDR'][0], chunk.raw_chunk_data)
        elif chunk.type == 'hIST':
            return hIST(chunk.raw_chunk_data)
        elif chunk.type == 'sPLT':
            return sPLT(chunk.raw_chunk_data)
        elif chunk.type == 'IEND':
            return IEND(chunk.raw_chunk_data)

    def print_headers(self):
        for item in self.chunks_dict.keys():
            print(item)

    def print_data(self):
        for item in self.chunks_dict.values():
            for chunk in item:
                if not chunk is None:
                    print(chunk.parsed_data)

    def print_headers_and_data(self):
        for item in self.chunks_dict.items():
            print(item[0])
            for chunk in item[1]:
                if not chunk is None:
                    print(chunk.parsed_data)
