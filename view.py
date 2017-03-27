import datetime


def list_partition(list):
    header("Part 1 Access an Image")
    for item in list:
        print item


def file_attributes(file):
    header("Part 2 Extract a file from an image")
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
