import datetime


def list_partition(list):
    header("Access an Image")

    if list is not None:
        for item in list:
            print item
    else:
        print 'No items'


def file_attributes(file):
    header("Extract a file from an image")
    print "File Inode:", file.get_inode()
    print "File Name:", file.get_name()
    print "File Creation Time:", datetime.datetime.fromtimestamp(file.get_file_creation()).strftime(
        '%Y-%m-%d %H:%M:%S')


def header(text):
    print '##################################################'
    print text
    print '##################################################'


def endView():
    print 'Goodbye!'
