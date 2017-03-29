import os

import psutil
import pytsk3
import pyewf
import pyvshadow

from model import vss
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

            file_name = ''

            if isinstance(self, DiskImage):
                file_name = self.file_path
                with open(file_name) as imageFile:
                    image_handle = pytsk3.Img_Info(imageFile.name)
                    self.set_handle(image_handle)

            elif isinstance(self, LiveImage):
                file_name = self.physical_drive
                image_handle = pytsk3.Img_Info(file_name)
                self.set_handle(image_handle)
                image_handle.close()
            elif isinstance(self, EWFImage):

                file_name = self.get_file_name()
                file_names = pyewf.glob(file_name)

                ewt_handle = pyewf.handle()
                ewt_handle.open(file_names)
                image_handle = ewf_Img_Info(ewt_handle)
                self.set_handle(image_handle)
            else:
                raise AttributeError('check class')

            partition_table = pytsk3.Volume_Info(self.get_handle())


            '''
            partitionList = psutil.disk_partitions()
            dirPath = "/"

            for partition2 in partitionList:
                imagehandle = pytsk3.Img_Info('\\\\.\\' + partition2.device.strip("\\"))
                filesystemObject = pytsk3.FS_Info(imagehandle)

                directoryObject = filesystemObject.open_dir(path=dirPath)
                print "SAB"
                print "Directory:", dirPath
                
            '''

            for partition in partition_table:

                p = Partition(partition.addr, partition.desc, partition.start, partition.len, self.get_handle())
                p.set_image_file(file_name)

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


class VolumeShadow(Image):

    def __init__(self, image_file):
        Image.__init__(self)
        self.image_file = os.path.expanduser(image_file)

    def get_image_file(self):
        return self.image_file