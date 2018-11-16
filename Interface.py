from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
import sys
from PngFile import PngFile


class MainWindow(QWidget):

    def __init__(self, filename):
        super().__init__()
        self.file = PngFile(filename)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Png')
        self.setFixedSize(500, 500)
        self.prepearing()
        self.show()

    def prepearing(self):
        self.Width = self.file.chunks_dict['IHDR'][0].parsed_data['Width']
        self.Height = self.file.chunks_dict['IHDR'][0].parsed_data['Height']
        self.Bit_depth = self.file.chunks_dict['IHDR'][0].parsed_data['Bit depth']
        self.Color_info = self.file.chunks_dict['IHDR'][0].parsed_data['Color info']
        self.Interlaced = self.file.chunks_dict['IHDR'][0].parsed_data['Interlace info']
        self.choose_variant_of_drawing()

    def choose_variant_of_drawing(self):
        if self.Color_info == 'Индексированные значения':
            self.update()

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        dict_of_pixels = self.file.chunks_dict['PLTE'][0].parsed_data
        list_of_pixels = self.file.chunks_dict['IDAT'][0].parsed_data['Result of decoding']
        for y in range(self.Height):
            for x in range(self.Width):
                pixel = dict_of_pixels[list_of_pixels[y][x]]
                color = QColor(pixel[0], pixel[1], pixel[2])
                qp.setPen(color)
                qp.setBrush(color)
                qp.drawRect(x * 10, y * 10, 10, 10)
        qp.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(sys.argv[1])
    sys.exit(app.exec_())
