class Partition:
    def __init__(self, address, description, start, length):
        self.address = address
        self.description = description
        self.start = start
        self.offset = self.get_offset()
        self.length = length

    def get_offset(self):
        return self.start * 512

    def get_description(self):
        return self.description

    '''
    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

        return ', '.join(sb)
    '''
    def __str__(self):
        return str(self.address) + " " + self.description + " " + str(self.start) + "s (" + str(self.get_offset()) + ") " + str(self.length)

        #print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len