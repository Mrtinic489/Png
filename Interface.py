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

        grid = QGridLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_layout = QFormLayout()

        picture = DrawWindow(self.Width, self.Height, self.Scale, self.List_of_pixels)
        picture.setMinimumSize(self.Width * 100, self.Height * 100)

        scroll_area.setWidget(picture)
        picture.setLayout(scroll_layout)

        button = QPushButton('RGB(A)')
        button.clicked.connect(self.button_clicked)

        grid.addWidget(scroll_area, 0, 0)
        grid.addWidget(button, 0, 1)
        self.setLayout(grid)
        self.show()

    def button_clicked(self):
        for y in range(self.Height):
            for x in range(self.Width):
                print('{0},{1} : {2}'.format(y, x, self.List_of_pixels[y][x]))

    def prepearing(self):
        self.Width = self.file.chunks_dict['IHDR'][0].parsed_data['Width']
        self.Height = self.file.chunks_dict['IHDR'][0].parsed_data['Height']
        self.Bit_depth = self.file.chunks_dict['IHDR'][0].parsed_data['Bit depth']
        self.Color_info = self.file.chunks_dict['IHDR'][0].parsed_data['Color info']
        self.Interlaced = self.file.chunks_dict['IHDR'][0].parsed_data['Interlace info']
        if self.Width <= 1 or self.Height <= 1:
            self.Scale = 16
        elif self.Width <= 2 or self.Height <= 2:
            self.Scale = 8
        elif self.Width <= 4 or self.Height <= 4:
            self.Scale = 4
        elif self.Width <= 8 or self.Height <= 8:
            self.Scale = 2
        else:
            self.Scale = 1
        self.List_of_pixels = self.file.chunks_dict['IDAT'][0].parsed_data['Result of decoding']


class DrawWindow(QWidget):

    def __init__(self, width, height, scale, list_of_pixels):
        super().__init__()
        self.Width = width
        self.Height = height
        self.Scale = scale
        self.List_of_pixels = list_of_pixels
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        for y in range(self.Height):
            for x in range(self.Width):
                pixel = self.List_of_pixels[y][x]
                color = QColor(*pixel)
                qp.setPen(color)
                qp.setBrush(color)
                qp.drawRect(x * self.Scale, y * self.Scale, self.Scale, self.Scale)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(sys.argv[1])
    sys.exit(app.exec_())
