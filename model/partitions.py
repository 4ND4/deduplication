import hashlib
import re

import pytsk3


class Partition:
    def __init__(self, address, description, start, length):
        self.address = address
        self.description = description
        self.start = start
        self.length = length
        self.handle = None

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

        file_system_object = pytsk3.FS_Info(self.get_handle(), offset=self.get_offset())
        directory_object = file_system_object.open_dir(path=dir_path)

        directoryRecurse(directory_object, [])

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
                directoryRecurseSearch(sub_directory, parentPath, search)
                parentPath.pop(-1)
                print "Directory: %s" % filePath

            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0:

                searchResult = re.match(search, entryObject.info.name.name)
                if not searchResult:
                    continue

                fileData = entryObject.read_random(0, entryObject.info.meta.size)

                print "match ", entryObject.info.name.name

                #sha1hash = hashlib.sha1()
                #sha1hash.update(fileData)
                #listObject.append(entryObject)

                #listSHA1.append(sha1hash.hexdigest())

                #print entryObject.info.name.name

        except IOError as e:
            print e
            continue