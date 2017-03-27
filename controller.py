from model import DiskImage
import view


def showAll():

    file_path = "~/Documents/UCD/Work/AssignmentImage.dmg"

    d = DiskImage(file_path)

    partitions_in_image = d.get_partitions()
    d.set_partitions(partitions_in_image)

    #d.write_file(2, "$MFT")
    #d.write_file(2, "$FAT")

    # calls view
    return view.list_partition(partitions_in_image)


def start():
    '''
    if input == 'y':
        return showAll()
    else:
        return view.endView()
    '''
    return showAll()