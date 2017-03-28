class File:
    def __init__(self, file):
        self.file = file
        self.inode = None
        self.name = None
        self.file_creation = None
        self.file_data = None

    def set_inode(self, inode):
        self.inode = inode

    def set_name(self, name):
        self.name = name

    def set_file_creation(self, file_creation):
        self.file_creation = file_creation

    def set_file_data(self, file_data):
        self.file_data = file_data

    def get_inode(self):
        return self.inode

    def get_name(self):
        return self.name

    def get_file_creation(self):
        return self.file_creation

    def get_file_data(self):
        return self.file_data

    def write(self):
        with open(self.file, 'w') as outfile:
            outfile.write(self.file_data)