import os
import pytsk3
import pyewf

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
                    self.set_handle(image_handle)

            elif isinstance(self, LiveImage):
                image_handle = pytsk3.Img_Info(self.physical_drive)
                self.set_handle(image_handle)
                image_handle.close()
            elif isinstance(self, EWFImage):

                file_names = pyewf.glob(self.get_file_name())

                ewt_handle = pyewf.handle()
                ewt_handle.open(file_names)
                image_handle = ewf_Img_Info(ewt_handle)
                self.set_handle(image_handle)

            else:
                raise AttributeError('check class')

            partition_table = pytsk3.Volume_Info(self.get_handle())

            for partition in partition_table:
                p = Partition(partition.addr, partition.desc, partition.start, partition.len)
                p.set_handle(self.get_handle())
                partitions.append(p)

            return partitions

        except IOError as e:
            print 'fail'
            print e.message
            return None

    def set_handle(self, handle):
        self.handle = handle

    def get_handle(self):
        return self.handle

    def set_partitions(self, partitions):
        self.partitions = partitions

    def get_offset_partition(self, address):

        partition = self.get_partition(address)

        if partition is not None:
            return int(partition.get_offset())
        return -1

    def get_partition(self, address):

        if self.partitions is not None:
            for partition in self.partitions:
                if partition.address == address:
                    return partition
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