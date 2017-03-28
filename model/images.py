import os
import pytsk3
import pyewf

from model.files import File
from model.partitions import Partition


class Image:
    def __init__(self):

        self.partitions = None
        self.size = None
        self.name = None
        self.type = None
        self.os = None
        self.url = None
        self.handle = None

    def get_partitions(self):

        partitions = []

        try:

            if isinstance(self, DiskImage):
                with open(self.file_path) as imageFile:
                    image_handle = pytsk3.Img_Info(imageFile.name)
            elif isinstance(self, LiveImage):
                image_handle = pytsk3.Img_Info(self.physical_drive)
                image_handle.close()
            elif isinstance(self, EWFImage):

                file_names = pyewf.glob(self.get_file_name())

                ewt_handle = pyewf.handle()
                ewt_handle.open(file_names)
                image_handle = ewf_Img_Info(ewt_handle)

            else:
                raise AttributeError('check class')

            partition_table = pytsk3.Volume_Info(image_handle)

            for partition in partition_table:
                partitions.append(Partition(partition.addr, partition.desc, partition.start, partition.len))

            return partitions

        except IOError as e:
            print 'fail'
            print e.message
            return None

    def set_partitions(self, partitions):
        self.partitions = partitions

    def get_offset_partition(self, address):

        if self.partitions is not None:
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


class DiskImage(Image):
    def __init__(self, file_path):
        Image.__init__(self)
        self.file_path = os.path.expanduser(file_path)


class LiveImage(Image):
    def __init__(self, physical_drive):
        Image.__init__(self)
        self.physical_drive = physical_drive


class ewf_Img_Info(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(ewf_Img_Info, self).__init__(
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()


class EWFImage(Image):

    def __init__(self, file_name):
        Image.__init__(self)
        self.file_name = os.path.expanduser(file_name)

    def get_file_name(self):
        return self.file_name