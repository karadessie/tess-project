class Multireader():
    def __init__(self, filename):
        self.filename = filename
        self.f = open(filename, 'rt')

    def close(self):
        self.f.close()

    def read(self):
        return self.f.read()