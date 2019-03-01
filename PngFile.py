from Chunk import Chunk
from Utils.Byte_parser import parse_bytes
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


class PngFile:

    def __init__(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.file = f.read()
                self.header = self.file[:8]
                if self.header[0] != 137 or \
                        self.header[1:4].decode('ascii') != 'PNG':
                    raise Exception('Not png')
        except Exception:
            raise Exception('Smth go wrong')
        self.list_of_chunks = []
        self.find_chunks()
        self.chunks_dict = dict()
        self.fill_in_dict()

    def find_chunks(self):
        try:
            index = 8
            while index < len(self.file):
                length = parse_bytes(self.file, [index, index + 4], False)[0]
                self.list_of_chunks.append(
                    Chunk(self.file[index:index + 12 + length]))
                index += 12 + length
        except Exception:
            pass

    def fill_in_dict(self):
        for chunk in self.list_of_chunks:
            if chunk.type not in self.chunks_dict.keys():
                self.chunks_dict[chunk.type] = []
            self.chunks_dict[chunk.type].append(self.parse_type(chunk))

    def parse_type(self, chunk):
        parser_dict = dict([('IHDR', IHDR), ('PLTE', PLTE), ('IDAT', IDAT),
                            ('iTXt', iTXt), ('tEXt', tEXt), ('zTXt', zTXt),
                            ('cHRM', cHRM), ('gAMA', gAMA), ('iCCP', iCCP),
                            ('sRGB', sRGB), ('bKGD', bKGD), ('tRNS', tRNS),
                            ('pHYs', pHYs), ('tIME', tIME), ('sBIT', sBIT),
                            ('hIST', hIST), ('sPLT', sPLT), ('IEND', IEND)])
        if chunk.type == 'IDAT':
            if 'PLTE' in self.chunks_dict.keys():
                return parser_dict[chunk.type](
                    self.chunks_dict['IHDR'][0], self.chunks_dict['PLTE'][0],
                    chunk.raw_chunk_data)
            else:
                return parser_dict[chunk.type](
                    self.chunks_dict['IHDR'][0], None, chunk.raw_chunk_data)
        if chunk.type == 'bKGD' or chunk.type == 'tRNS' or \
                chunk.type == 'sBIT':
            return parser_dict[chunk.type](
                self.chunks_dict['IHDR'][0], chunk.raw_chunk_data)
        else:
            return parser_dict[chunk.type](
                chunk.raw_chunk_data)

    def print_headers(self):
        for key, chunks in self.chunks_dict.items():
            if key != 'IDAT':
                print(key)
                for chunk in chunks:
                    for key, value in chunk.parsed_data.items():
                        print('{0} : {1}'.format(key, value))
                print()

    def print_data(self):
        list_of_pixels = \
            self.chunks_dict['IDAT'][0].parsed_data['Result of decoding']
        for line in list_of_pixels:
            for pixel in line:
                print(*pixel)

    def print_headers_and_data(self):
        self.print_headers()
        self.print_data()
