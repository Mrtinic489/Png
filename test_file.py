#!/usr/bin/env python3
import unittest
from Chunk import Chunk
from PngFile import PngFile


class Test(unittest.TestCase):

    def test_for_init(self):
        png_file = PngFile('TestPictures/basi0g01.png')
        self.assertTrue(len(png_file.list_of_raw_chunks) != 0)
        self.assertTrue(Chunk(png_file.list_of_raw_chunks[0]).type == 'IHDR')
        self.assertTrue(Chunk(png_file.list_of_raw_chunks[-1]).type == 'IEND')

    def test_for_ihdranalize(self):
        png_file = PngFile('TestPictures/basi0g01.png')
        self.assertTrue(png_file.IHDRchunk.data_dict['Width'] == 32)
        self.assertTrue(png_file.IHDRchunk.data_dict['Height'] == 32)
        self.assertTrue(png_file.IHDRchunk.data_dict['Bit depth'] == 1)
        self.assertTrue(png_file.IHDRchunk.data_dict['Color info'] == 'Grayscale')
        self.assertTrue(png_file.IHDRchunk.data_dict['Compress method'] == 'Deflate compress method')
        self.assertTrue(png_file.IHDRchunk.data_dict['Filter method'] == 'Correct')
        self.assertTrue(png_file.IHDRchunk.data_dict['Interlace info'] == 'Adam7 interlace')

        png_file = PngFile('TestPictures/basi0g02.png')
        self.assertTrue(png_file.IHDRchunk.data_dict['Bit depth'] == 2)

        png_file = PngFile('TestPictures/basi0g04.png')
        self.assertTrue(png_file.IHDRchunk.data_dict['Bit depth'] == 4)

        png_file = PngFile('TestPictures/basi2c08.png')
        self.assertTrue(png_file.IHDRchunk.data_dict['Color info'] == 'RGB')

        png_file = PngFile('TestPictures/basi3p01.png')
        self.assertTrue(png_file.IHDRchunk.data_dict['Color info'] == 'Индексированные значения')

        png_file = PngFile('TestPictures/basi4a08.png')
        self.assertTrue(png_file.IHDRchunk.data_dict['Color info'] == 'Grayscale + alpha channel')

        png_file = PngFile('TestPictures/basi6a16.png')
        self.assertTrue(png_file.IHDRchunk.data_dict['Color info'] == 'RGBA')

    def test_for_iendanalize(self):
        png_file = PngFile('TestPictures/basn0g01.png')
        self.assertTrue(png_file.IENDchunk.data_dict['State'] == 'Correct')

    def test_for_idatanalize(self):
        png_file = PngFile('TestPictures/basn0g01.png')
        self.assertTrue(png_file.IDATchunk.data_dict['CM'] == 'Deflate compression method')
        self.assertTrue(png_file.IDATchunk.data_dict['Window size'] == '32768 bytes')
        self.assertTrue(png_file.IDATchunk.data_dict['FLEVEL'] == 'Default compression')
        self.assertTrue(png_file.IDATchunk.data_dict['FDICT'] == 'No dict')
        self.assertTrue(png_file.IDATchunk.data_dict['FCHECK'] == 'Correct')