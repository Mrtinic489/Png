from Utils.Byte_parser import parse_bytes


class IHDR:

    def __init__(self, byte_data):
        self.byte_data = byte_data
        self.parsed_data = dict()
        self.analize()

    def analize(self):
        from_bytes = parse_bytes(self.byte_data, [0, 4, 8], False)
        self.parsed_data['Width'] = from_bytes[0]
        self.parsed_data['Height'] = from_bytes[1]
        self.parsed_data['Bit depth'] = self.byte_data[8]
        color_info = self.byte_data[9]
        if color_info == 0:
            self.parsed_data['Color info'] = 'Grayscale'
        elif color_info == 2:
            self.parsed_data['Color info'] = 'RGB'
        elif color_info == 3:
            self.parsed_data['Color info'] = 'Индексированные значения'
        elif color_info == 4:
            self.parsed_data['Color info'] = 'Grayscale + alpha channel'
        elif color_info == 6:
            self.parsed_data['Color info'] = 'RGBA'
        if self.byte_data[10] == 0:
            self.parsed_data['Compress method'] = 'Deflate compress method'
        if self.byte_data[11] == 0:
            self.parsed_data['Filter method'] = 'Correct'
        if self.byte_data[12] == 0:
            self.parsed_data['Interlace info'] = 'No interlace'
        else:
            self.parsed_data['Interlace info'] = 'Adam7 interlace'
