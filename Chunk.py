class Chunk:
    def __init__(self, bytestr):
        self.length = int.from_bytes(bytestr[:4], 'big')
        self.type = bytestr[4:8].decode()
        self.raw_chunk_data = bytestr[8: 8 + self.length]
        self.crc = bytestr[8 + self.length:]
