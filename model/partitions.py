import hashlib
import os
import re

import pytsk3
import pyvshadow

import vss

class Partition:
    def __init__(self, address, description, start, length, handle):
        self.address = address
        self.description = description
        self.start = start
        self.length = length
        self.handle = handle
        self.type = None
        self.image_file = None

        self.set_type()

    def get_image_file(self):
        return self.image_file

    def set_image_file(self, image_file):
        self.image_file = image_file

    def get_address(self):
        return self.address

    def get_offset(self):
        return self.start * 512

    def get_description(self):
        return self.description

    def get_start(self):
        return self.start

    def get_length(self):
        return self.length

    def set_handle(self, handle):
        self.handle = handle

    def get_handle(self):
        return self.handle

    def __str__(self):
        return str(self.get_address()) + " " + \
               self.get_description() + " " + \
               str(self.get_start()) + "s (" + \
               str(self.get_offset()) + ") " + \
               str(self.get_length())

    def set_type(self):

        try:
            file_system_object = pytsk3.FS_Info(self.get_handle(), offset=self.get_offset())
            self.type = file_system_object.info.ftype
        except:
            print 'Warning ! Partition(' + str(self.get_address()) + ')' + self.get_description() + ' has no supported file system'

    def get_type(self):
        return self.type

    def extract_file(self, filename):

        file_system_object = pytsk3.FS_Info(self.get_handle(), offset=self.get_offset())

        try:
            fileobject = file_system_object.open("/" + filename)

            from model.files import File
            f = File(filename)
            f.set_inode(fileobject.info.meta.addr)
            f.set_name(fileobject.info.name.name)
            f.set_file_creation(fileobject.info.meta.crtime)

            file_data = fileobject.read_random(0, fileobject.info.meta.size)

            md5hash = hashlib.md5()
            md5hash.update(file_data)

            sha1hash = hashlib.sha1()
            sha1hash.update(file_data)

            f.set_md5hash(md5hash.hexdigest())
            f.set_sha1hash(sha1hash.hexdigest())

            f.set_file_data(file_data)

            return f

        except Exception as e:
            print e.message
            return None

    def list_files(self):

        dir_path = "/"

        #check if it's NTFS

        if self.get_type() is not None:

            file_system_object = pytsk3.FS_Info(self.get_handle(), offset=self.get_offset())

            if (str(self.get_type()) == "TSK_FS_TYPE_NTFS_DETECT"):
                print "NTFS DETECTED"

                volume = pyvshadow.volume()

                fh = vss.VShadowVolume(self.get_image_file(), self.get_offset())
                count = vss.GetVssStoreCount(self.get_image_file(), self.get_offset())
                if (count):
                    vstore = 0
                    volume.open_file_object(fh)
                    while (vstore < count):
                        store = volume.get_store(vstore)
                        img = vss.VShadowImgInfo(store)
                        vssfilesystemObject = pytsk3.FS_Info(img)
                        vssdirectoryObject = vssfilesystemObject.open_dir(path=dir_path)
                        print "Directory:", "vss", str(vstore), dir_path
                        directoryRecurse(vssdirectoryObject, ['vss', str(vstore)])
                        vstore = vstore + 1
                    # Capture the live volume
                    directory_object = file_system_object.open_dir(path=dir_path)
                    print "Directory:", dir_path

                    directoryRecurse(directory_object, [])

            else:

                directory_object = file_system_object.open_dir(path=dir_path)
                print "Directory:", dir_path
                directoryRecurse(directory_object, [])

        else:
            print 'No supported file system'


    def search_files(self, search_query):

        dir_path = "/"

        file_system_object = pytsk3.FS_Info(self.get_handle(), offset=self.get_offset())
        directory_object = file_system_object.open_dir(path=dir_path)

        directoryRecurseSearch(directory_object, [], search_query)


def directoryRecurse(directoryObject, parentPath):
    for entryObject in directoryObject:
        if entryObject.info.name.name in [".", ".."]:
            continue

        try:
            f_type = entryObject.info.meta.type
        except:
            print "Cannot retrieve type of", entryObject.info.name.name
            continue

        try:

            filePath = '/%s/%s' % ('/'.join(parentPath), entryObject.info.name.name)

            if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
                sub_directory = entryObject.as_directory()
                parentPath.append(entryObject.info.name.name)
                directoryRecurse(sub_directory, parentPath)
                parentPath.pop(-1)
                print "Directory: %s" % filePath

            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0:

                fileData = entryObject.read_random(0, entryObject.info.meta.size)

                #sha1hash = hashlib.sha1()
                #sha1hash.update(fileData)
                #listObject.append(entryObject)

                #listSHA1.append(sha1hash.hexdigest())

                #print entryObject.info.name.name


        except IOError as e:
            print e
            continue

def directoryRecurseSearch(directoryObject, parentPath, search):
    for entryObject in directoryObject:
        if entryObject.info.name.name in [".", ".."]:
            continue
        #print entryObject.info.name.name
        try:
            f_type = entryObject.info.meta.type
            size = entryObject.info.meta.size
        except Exception as error:
            print "Cannot retrieve type of", entryObject.info.name.name
            print error.message
            continue

        try:

            file_path = '/%s/%s' % ('/'.join(parentPath), entryObject.info.name.name)
            outputPath = './%s/' % ('/'.join(parentPath))

            if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
                sub_directory = entryObject.as_directory()
                print "Entering Directory: %s" % file_path
                parentPath.append(entryObject.info.name.name)
                directoryRecurseSearch(sub_directory, parentPath, search)
                parentPath.pop(-1)
                print "Leaving Directory: %s" % file_path

            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0:

                searchResult = re.match(search, entryObject.info.name.name)
                if not searchResult:
                    continue

                BUFF_SIZE = 1024 * 1024
                offset = 0

                if not os.path.exists(outputPath):
                    os.makedirs(outputPath)
                extractFile = open(outputPath + entryObject.info.name.name, 'w')
                while offset < entryObject.info.meta.size:
                    available_to_read = min(BUFF_SIZE, entryObject.info.meta.size - offset)
                    fileData = entryObject.read_random(offset, available_to_read)
                    #md5hash.update(filedata)
                    #sha1hash.update(filedata)
                    offset += len(fileData)

                    extractFile.write(fileData)


                #fileData = entryObject.read_random(0, entryObject.info.meta.size)

                print "match ", entryObject.info.name.name

                #sha1hash = hashlib.sha1()
                #sha1hash.update(fileData)
                #listObject.append(entryObject)

                #listSHA1.append(sha1hash.hexdigest())

                #print entryObject.info.name.name

        except IOError as e:
            print e
            continue