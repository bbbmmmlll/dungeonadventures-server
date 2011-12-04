#!/usr/bin/python

"""Generate Monster."""
import sys
import random
import pickle

class Monster(object):
    """"""

    def __init__(self):
        self.name = "generic monster"

    def show(self):
        pass

    def save(self):
        name = "../data/%s.monster" % (self.name)
        fh = open(name, 'wb')
        if fh:
            pickle.dump(self, fh, 2)
            fh.close()

    def getsizeof(self):
        size = sys.getsizeof(self)
        return size


if __name__ == "__main__":
    random.seed()
    obj = Monster("test monster")
    obj.show()
    print "sizeof monster: %d bytes" % (obj.getsizeof())
    obj.save()
