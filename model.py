import pytsk3
import os


class DiskImage:

    def __init__(self, file_path):

        self.partitions = None
        self.size = None
        self.name = None
        self.type = None
        self.os = None
        self.file_path = os.path.expanduser(file_path)

    def get_partitions(self):

        partitions = []

        with open(self.file_path) as imageFile:
            image_handle = pytsk3.Img_Info(imageFile.name)

        partition_table = pytsk3.Volume_Info(image_handle)

        for partition in partition_table:
            partitions.append(Partition(partition.addr, partition.desc, partition.start, partition.len))

        return partitions

    def set_partitions(self, partitions):
        self.partitions = partitions

    def get_offset_partition(self, address):

        for partition in self.partitions:
            if partition.address == address:
                return int(partition.get_offset())
        return -1

    def extract_file(self, address, filename):
        with open(self.file_path) as imageFile:
            image_handle = pytsk3.Img_Info(imageFile.name)

            ofs = self.get_offset_partition(address)

            if ofs > 0:
                file_system_object = pytsk3.FS_Info(image_handle, offset=ofs)
                fileobject = file_system_object.open("/" + filename)

                f = File(filename)
                f.set_inode(fileobject.info.meta.addr)
                f.set_name(fileobject.info.name.name)
                f.set_file_creation(fileobject.info.meta.crtime)

                file_data = fileobject.read_random(0, fileobject.info.meta.size)

                f.set_file_data(file_data)

                return f
            else:
                print 'error getting offset'
                return None


class Partition:
    def __init__(self, address, description, start, length):
        self.address = address
        self.description = description
        self.start = start
        self.offset = self.get_offset()
        self.length = length

    def get_offset(self):
        return self.start * 512

    def get_description(self):
        return self.description

    '''
    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

        return ', '.join(sb)
    '''
    def __str__(self):
        return str(self.address) + " " + self.description + " " + str(self.start) + "s (" + str(self.get_offset()) + ") " + str(self.length)

        #print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len


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
