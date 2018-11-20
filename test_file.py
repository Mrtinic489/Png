import unittest
from Chunk import Chunk
from PngFile import PngFile


class Test(unittest.TestCase):

    def test_for_init(self):
        png_file = PngFile('TestPictures/basi0g01.png')
        self.assertEqual(len(png_file.chunks_dict.keys()), 4)
        self.assertTrue('IHDR' in png_file.chunks_dict.keys())
        self.assertTrue('IEND' in png_file.chunks_dict.keys())

    def test_for_ihdranalize(self):
        png_file = PngFile('TestPictures/basi0g01.png')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Width'], 32)
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Height'], 32)
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Bit depth'], 1)
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Color info'], 'Grayscale')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Compress method'], 'Deflate compress method')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Filter method'], 'Correct')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Interlace info'], 'Adam7 interlace')

        png_file = PngFile('TestPictures/basi0g02.png')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Bit depth'], 2)

        png_file = PngFile('TestPictures/basi0g04.png')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Bit depth'], 4)

        png_file = PngFile('TestPictures/basi2c08.png')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Color info'], 'RGB')

        png_file = PngFile('TestPictures/basi3p01.png')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Color info'], 'Индексированные значения')

        png_file = PngFile('TestPictures/basi4a08.png')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Color info'], 'Grayscale + alpha channel')

        png_file = PngFile('TestPictures/basi6a16.png')
        self.assertEqual(png_file.chunks_dict['IHDR'][0].parsed_data['Color info'], 'RGBA')

    def test_for_iendanalize(self):
        png_file = PngFile('TestPictures/basn0g01.png')
        self.assertEqual(png_file.chunks_dict['IEND'][0].parsed_data['State'], 'Correct')

    def test_for_plteanalize(self):
        png_file = PngFile('TestPictures/s01i3p01.png')
        for item in png_file.chunks_dict.keys():
            if item == 'PLTE':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data[0], tuple([0, 0, 255]))

        png_file = PngFile('TestPictures/s03i3p01.png')
        for item in png_file.chunks_dict.keys():
            if item == 'PLTE':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data[0], tuple([0, 255, 0]))
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data[1], tuple([255, 119, 0]))

    def test_for_bgkdanalize(self):
        png_file = PngFile('TestPictures/bgbn4a08.png')
        for item in png_file.chunks_dict.keys():
            if item == 'bKGD':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Gray bKGD'], 0)

        png_file = PngFile('TestPictures/bgwn6a08.png')
        for item in png_file.chunks_dict.keys():
            if item == 'bKGD':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Red bKGD'], 255)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Green bKGD'], 255)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Blue bKGD'], 255)

    def test_for_gamaanalize(self):
        png_file = PngFile('TestPictures/g04n0g16.png')
        for item in png_file.chunks_dict.keys():
            if item == 'gAMA':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Gamma value'], 0.45)

        png_file = PngFile('TestPictures/g07n0g16.png')
        for item in png_file.chunks_dict.keys():
            if item == 'gAMA':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Gamma value'], 0.7)

    def test_for_timeanalize(self):
        png_file = PngFile('TestPictures/cm0n0g04.png')
        for item in png_file.chunks_dict.keys():
            if item == 'tIME':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Year'], 2000)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Month'], 1)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Day'], 1)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Hour'], 12)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Minute'], 34)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Second'], 56)

        png_file = PngFile('TestPictures/cm7n0g04.png')
        for item in png_file.chunks_dict.keys():
            if item == 'tIME':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Year'], 1970)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Month'], 1)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Day'], 1)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Hour'], 0)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Minute'], 0)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Second'], 0)

    def test_for_physanalize(self):
        png_file = PngFile('TestPictures/cdfn2c08.png')
        for item in png_file.chunks_dict.keys():
            if item == 'pHYs':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Unit specifire'], 0)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Pixels per unknow unit, X'], 1)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Pixels per unknow unit, Y'], 4)

        png_file = PngFile('TestPictures/cdun2c08.png')
        for item in png_file.chunks_dict.keys():
            if item == 'pHYs':
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Unit specifire'], 1)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Pixels per meter, X'], 1000)
                self.assertEqual(png_file.chunks_dict[item][0].parsed_data['Pixels per meter, Y'], 1000)