#!/usr/bin/python

"""Generate Trap."""
import sys
import random
import pickle

class Trap(object):
    """"""

    def __init__(self):
        self.name = "generic trap"

    def show(self):
        pass

    def save(self):
        name = "../data/%s.trap" % (self.name)
        fh = open(name, 'wb')
        if fh:
            pickle.dump(self, fh, 2)
            fh.close()

    def getsizeof(self):
        size = sys.getsizeof(self)
        return size


if __name__ == "__main__":
    random.seed()
    obj = Monster("test trap")
    obj.show()
    print "sizeof trap: %d bytes" % (obj.getsizeof())
    obj.save()
