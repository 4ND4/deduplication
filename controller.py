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

    # Part 5 Auto escalating

    '''
    import admin,sys

    if not admin.isUserAdmin():
        admin.runAsAdmin()
        sys.exit
        
    '''

    # file_path = "~/Documents/UCD/Work/AssignmentImage.dmg" #macOS
    file_path = "D:/Forensics/AssignmentImage.dmg"  # windowsOS

    disk_image = DiskImage(file_path)

    # Part 1 Access an Image
    show_partitions(disk_image)

    # Part 2 Extract a file from an image

    # for NTFS we can use:
    # file_extraction = "$MFT"

    file_extraction = ".Trashes"
    show_file_attributes(disk_image, file_extraction)

    # Part 3 Extracting a file from a live system
    # windowsOS

    # mount drive with ftk imager
    physical_drive = "\\\\.\\PhysicalDrive3"

    physical_disk_image = LiveImage(physical_drive)
    show_partitions(physical_disk_image)

    # Part 4 Turn python program into a windows executable

    #done check setup.py

    # Part 5 (Check beginning)

    # Part 6

    import pyewf

    file_path = "D:/Forensics/SSFCC-Level5.E01"  # windowsOS

    disk_image = EWFImage(file_path)

    show_partitions(disk_image)

    filenames = pyewf.glob(file_path)

    ewf_handle = pyewf.handle()

    ewf_handle.open(filenames)

    imagehandle = ewf_Img_Info(ewf_handle)