class File:
    def __init__(self, file_name):
        self.file = file_name
        self.inode = None
        self.name = None
        self.file_creation = None
        self.file_data = None
        self.md5hash = None
        self.sha1hash = None

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

    def set_md5hash(self, md5hash):
        self.md5hash = md5hash

    def get_md5hash(self):
        return self.md5hash

    def set_sha1hash(self, sha1hash):
        self.sha1hash = sha1hash

    def get_sha1hash(self):
        return self.sha1hash


class Search:
    def __init__(self, query):
        self.query = query

    def get_query(self):
        return self.query