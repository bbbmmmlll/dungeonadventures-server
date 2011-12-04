#!/usr/bin/python

"""Generate Room."""
import sys
import random
import pickle

class Room(object):
    """"""

    def __init__(self,id):
        self.name = "generic room"
        self.id = id
        self.col = row
        self.row = col
        self.monster = 0
        self.treasure = 0
        self.trap = 0
        self.artifact = 0
        self.up = 0
        self.down = 0

    def show(self):
        pass

    def save(self):
        name = "../data/%s.room" % (self.name)
        fh = open(name, 'wb')
        if fh:
            pickle.dump(self, fh, 2)
            fh.close()

    def getsizeof(self):
        size = sys.getsizeof(self)
        return size


if __name__ == "__main__":
    random.seed()
    obj = Room("test room")
    obj.show()
    print "sizeof room: %d bytes" % (obj.getsizeof())
    obj.save()
