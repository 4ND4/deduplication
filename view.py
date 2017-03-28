import datetime


def list_partition(list):
    header("Access an Image")

    if list is not None:
        for item in list:
            print item
    else:
        print 'No items'


def file_attributes(file_name):
    if file_name is not None:
        header("Extract a file from an image")
        print "File Inode:", file_name.get_inode()
        print "File Name:", file_name.get_name()
        print "File Creation Time:", datetime.datetime.fromtimestamp(file_name.get_file_creation()).strftime(
            '%Y-%m-%d %H:%M:%S')
    else:
        print 'File not found'


def header(text):
    print '##################################################'
    print text
    print '##################################################'


def endView():
    print 'Goodbye!'
