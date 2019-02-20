from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
import sys
from PngFile import PngFile
import pyqtgraph


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
        scroll_area.setWidget(picture)
        picture.setMinimumSize(self.Width * self.Scale, self.Height * self.Scale)
        picture.setLayout(scroll_layout)
        scroll_area_for_rgb_info = QScrollArea()
        scroll_area_for_rgb_info.setWidgetResizable(True)
        scroll_area_for_rgb_info.setMinimumSize(150, 150)
        rgb_info_window = RGBInfoWindow(self.List_of_pixels)
        scroll_area_for_rgb_info.setWidget(rgb_info_window)
        grid.addWidget(scroll_area, 0, 0, 2, 2)
        grid.addWidget(scroll_area_for_rgb_info, 0, 2)
        if sys.argv[-1] == '--hist':
            channel_hist = HistogrammInfo(self.List_of_pixels, 'ALL')
            grid.addWidget(channel_hist, 1, 2)

            r_hist = HistogrammInfo(self.List_of_pixels, 'R')
            grid.addWidget(r_hist, 2, 0)

            g_hist = HistogrammInfo(self.List_of_pixels, 'G')
            grid.addWidget(g_hist, 2, 1)

            b_hist = HistogrammInfo(self.List_of_pixels, 'B')
            grid.addWidget(b_hist, 2, 2)

        self.setLayout(grid)
        self.setWindowTitle('Scale:{}'.format(self.Scale))
        self.show()

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
                if len(pixel) == 3:
                    color = QColor(*pixel)
                else:
                    color = QColor(pixel[1], pixel[2], pixel[3], pixel[0])
                qp.setPen(color)
                qp.setBrush(color)
                qp.drawRect(x * self.Scale, y * self.Scale, self.Scale, self.Scale)


class RGBInfoWindow(QWidget):

    def __init__(self, list_of_pixels):
        super().__init__()
        self.list_of_pixels = list_of_pixels
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        count = 0
        for y in range(len(self.list_of_pixels)):
            for x in range(len(self.list_of_pixels[0])):
                self.grid.addWidget(QLabel('Y:{0}, X:{1} : {2}'.format(y, x, self.list_of_pixels[y][x])), count, 0)
                count += 1
        self.setLayout(self.grid)
        self.show()


class HistogrammInfo(QWidget):

    def __init__(self, list_of_pixels, type_of_hist):
        super().__init__()
        self.list_of_pixels = list_of_pixels
        self.type_of_hist = type_of_hist
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.creating_data()
        plot = pyqtgraph.PlotWidget()
        if self.type_of_hist == 'ALL':
            brush = (150, 150, 150)
        elif self.type_of_hist == 'R':
            brush = (255, 0, 0, 80)
        elif self.type_of_hist == 'G':
            brush = (0, 255, 0, 80)
        else:
            brush = (0, 0, 255, 80)
        curve = pyqtgraph.PlotCurveItem([i for i in range(257)], self.data, stepMode=True, fillLevel=0, brush=brush)
        plot.addItem(curve)
        self.grid.addWidget(plot)
        self.setLayout(self.grid)
        self.show()

    def creating_data(self):
        self.data = [0 for i in range(256)]
        if self.type_of_hist == 'R':
            index = 0
        elif self.type_of_hist == 'G':
             index = 1
        elif self.type_of_hist == 'B':
             index = 2
        else:
             index = 'ALL'
        for row in self.list_of_pixels:
            for pixel in row:
                if type(index) == str:
                    print(pixel)
                    self.data[sum([pixel[i] for i in range(len(pixel) - 1)]) // 3] += 1
                else:
                    self.data[pixel[index]] += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(sys.argv[1])
    sys.exit(app.exec_())
