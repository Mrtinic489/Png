import unittest
from Chunk import Chunk
from PngFile import PngFile


class Test(unittest.TestCase):

    def test_for_init(self):
        png_file = PngFile('TestPictures/basi0g01.png')
        self.assertEqual(len(png_file.list_of_chunks), 4)
        self.assertEqual(Chunk(png_file.list_of_chunks[0]).type, 'IHDR')
        self.assertEqual(Chunk(png_file.list_of_chunks[-1]).type, 'IEND')

    def test_for_ihdranalize(self):
        png_file = PngFile('TestPictures/basi0g01.png')
        self.assertEqual(png_file.IHDRchunk.data_dict['Width'], 32)
        self.assertEqual(png_file.IHDRchunk.data_dict['Height'], 32)
        self.assertEqual(png_file.IHDRchunk.data_dict['Bit depth'], 1)
        self.assertEqual(png_file.IHDRchunk.data_dict['Color info'], 'Grayscale')
        self.assertEqual(png_file.IHDRchunk.data_dict['Compress method'], 'Deflate compress method')
        self.assertEqual(png_file.IHDRchunk.data_dict['Filter method'], 'Correct')
        self.assertEqual(png_file.IHDRchunk.data_dict['Interlace info'], 'Adam7 interlace')

        png_file = PngFile('TestPictures/basi0g02.png')
        self.assertEqual(png_file.IHDRchunk.data_dict['Bit depth'], 2)

        png_file = PngFile('TestPictures/basi0g04.png')
        self.assertEqual(png_file.IHDRchunk.data_dict['Bit depth'], 4)

        png_file = PngFile('TestPictures/basi2c08.png')
        self.assertEqual(png_file.IHDRchunk.data_dict['Color info'], 'RGB')

        png_file = PngFile('TestPictures/basi3p01.png')
        self.assertEqual(png_file.IHDRchunk.data_dict['Color info'], 'Индексированные значения')

        png_file = PngFile('TestPictures/basi4a08.png')
        self.assertEqual(png_file.IHDRchunk.data_dict['Color info'], 'Grayscale + alpha channel')

        png_file = PngFile('TestPictures/basi6a16.png')
        self.assertEqual(png_file.IHDRchunk.data_dict['Color info'], 'RGBA')

    def test_for_iendanalize(self):
        png_file = PngFile('TestPictures/basn0g01.png')
        self.assertEqual(png_file.decoded_chunks[-1].data_dict['State'], 'Correct')

    def test_for_plteanalize(self):
        png_file = PngFile('TestPictures/s01i3p01.png')
        for item in png_file.decoded_chunks:
            if item.type == 'PLTE':
                self.assertEqual(item.data_dict[0], tuple([0, 0, 255]))

        png_file = PngFile('TestPictures/s03i3p01.png')
        for item in png_file.decoded_chunks:
            if item.type == 'PLTE':
                self.assertEqual(item.data_dict[0], tuple([0, 255, 0]))
                self.assertEqual(item.data_dict[1], tuple([255, 119, 0]))

    def test_for_bgkdanalize(self):
        png_file = PngFile('TestPictures/bgbn4a08.png')
        for item in png_file.decoded_chunks:
            if item.type == 'bKGD':
                self.assertEqual(item.data_dict['Gray'], 0)

        png_file = PngFile('TestPictures/bgwn6a08.png')
        for item in png_file.decoded_chunks:
            if item.type == 'bKGD':
                self.assertEqual(item.data_dict['Red'], 255)
                self.assertEqual(item.data_dict['Green'], 255)
                self.assertEqual(item.data_dict['Blue'], 255)

    def test_for_gamaanalize(self):
        png_file = PngFile('TestPictures/g04n0g16.png')
        for item in png_file.decoded_chunks:
            if item.type == 'gAMA':
                self.assertEqual(item.data_dict['Gamma value'], 0.45)

        png_file = PngFile('TestPictures/g07n0g16.png')
        for item in png_file.decoded_chunks:
            if item.type == 'gAMA':
                self.assertEqual(item.data_dict['Gamma value'], 0.7)

    def test_for_trnsanalize(self):
        png_file = PngFile('TestPictures/tbwn3p08.png')
        for item in png_file.decoded_chunks:
            if item.type == 'tRNS':
                self.assertEqual(item.data_dict['Alpha for index 0'], 0)

        png_file = PngFile('TestPictures/tm3n3p02.png')
        for item in png_file.decoded_chunks:
            if item.type == 'tRNS':
                self.assertEqual(item.data_dict['Alpha for index 0'], 0)
                self.assertEqual(item.data_dict['Alpha for index 1'], 85)
                self.assertEqual(item.data_dict['Alpha for index 2'], 170)

    def test_for_timeanalize(self):
        png_file = PngFile('TestPictures/cm0n0g04.png')
        for item in png_file.decoded_chunks:
            if item.type == 'tIME':
                self.assertEqual(item.data_dict['Year'], 2000)
                self.assertEqual(item.data_dict['Month'], 1)
                self.assertEqual(item.data_dict['Day'], 1)
                self.assertEqual(item.data_dict['Hour'], 12)
                self.assertEqual(item.data_dict['Minute'], 34)
                self.assertEqual(item.data_dict['Second'], 56)

        png_file = PngFile('TestPictures/cm7n0g04.png')
        for item in png_file.decoded_chunks:
            if item.type == 'tIME':
                self.assertEqual(item.data_dict['Year'], 1970)
                self.assertEqual(item.data_dict['Month'], 1)
                self.assertEqual(item.data_dict['Day'], 1)
                self.assertEqual(item.data_dict['Hour'], 0)
                self.assertEqual(item.data_dict['Minute'], 0)
                self.assertEqual(item.data_dict['Second'], 0)

    def test_for_physanalize(self):
        png_file = PngFile('TestPictures/cdfn2c08.png')
        for item in png_file.decoded_chunks:
            if item.type == 'pHYs':
                self.assertEqual(item.data_dict['Unit specifire'], 0)
                self.assertEqual(item.data_dict['Pixels per unknow unit, X'], 1)
                self.assertEqual(item.data_dict['Pixels per unknow unit, Y'], 4)

        png_file = PngFile('TestPictures/cdun2c08.png')
        for item in png_file.decoded_chunks:
            if item.type == 'pHYs':
                self.assertEqual(item.data_dict['Unit specifire'], 1)
                self.assertEqual(item.data_dict['Pixels per meter, X'], 1000)
                self.assertEqual(item.data_dict['Pixels per meter, Y'], 1000)