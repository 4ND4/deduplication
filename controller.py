from model.images import DiskImage, LiveImage, EWFImage

import view


def show_partitions(disk_image):
    partitions_in_image = disk_image.get_partitions()
    # set partitions to image
    disk_image.set_partitions(partitions_in_image)
    # calls view
    return view.list_partition(partitions_in_image)


def show_file_attributes(disk_image, file_extraction):
    f = disk_image.extract_file(2, file_extraction)
    f.write()

    return view.file_attributes(f)


def start():

    # Part 5 Auto escalating (Uncomment)

    '''
    import admin,sys

    if not admin.isUserAdmin():
        admin.runAsAdmin()
        sys.exit
        
    '''

    # file_path = "~/Documents/UCD/Work/AssignmentImage.dmg" #macOS
    # file_path = "D:/Forensics/AssignmentImage.dmg"  # windowsOS
    file_path = "/media/felix/DATA/Forensics/AssignmentImage.dmg"   #linuxOS

    disk_image = DiskImage(file_path)

    # Part 1 Access an Image
    print 'Part 1'
    show_partitions(disk_image)

    # Part 2 Extract a file from an image
    print 'Part 2'

    # for NTFS we can use:
    # file_extraction = "$MFT"

    file_extraction = ".Trashes"
    show_file_attributes(disk_image, file_extraction)

    # Part 3 Extracting a file from a live system
    # windowsOS

    print 'Part 3'

    # mount drive with ftk imager
    physical_drive = "\\\\.\\PhysicalDrive3"

    physical_disk_image = LiveImage(physical_drive)
    show_partitions(physical_disk_image)

    # Part 4 Turn python program into a windows executable

    #done check setup.py

    # Part 5 (Check beginning)

    # Part 6

    print 'Part 6'

    #file_name = "D:/Forensics/image.E01"  # windowsOS
    file_name = "/media/felix/DATA/Forensics/image.E01" #linuxOS

    disk_image = EWFImage(file_name)

    show_partitions(disk_image)


def start_args():

    # Part 6

    print 'Part 6'

    import argparse

    argparser = argparse.ArgumentParser(description="Extract the $MFT from all of the NTFS partitions of an E01")

    argparser.add_argument(
        '-i', '--image',
        dest='imagefile',
        action="store",
        type=str,
        default=None,
        required=True,
        help='E01 to extract from'
    )

    args = argparser.parse_args()

    file_name = args.imagefile
    disk_image = EWFImage(file_name)
    show_partitions(disk_image)