#!/usr/bin/python

"""Generate Game Level."""
import sys
import random
import pickle
import datetime
import pymongo
from pymongo import Connection
from pymongo.errors import ConnectionFailure

LEVEL_COLS = 10
LEVEL_ROWS = 10
MIN_ROOMS = 17
MAX_ROOMS = 30
STAIRS_DOWN = 2
STAIRS_UP = 2

class Level(object):
    """"""

    def __init__(self,id):
        self.id = id
        self.room_count = 0
        # list of lists: probably a better way to do this
        self.level_map = [[0 for row in range(LEVEL_ROWS)] for col in range(LEVEL_COLS)] 
        self.level_dict = dict()
        self.level_dict["rooms"] = dict()

        # generate level
        # start by making a random seed room
        self.rooms = [] 
        room_id = 1
        row = random.randint(2,LEVEL_ROWS-3)
        col = random.randint(2,LEVEL_COLS-3)
        self.level_map[row][col] = room_id
        self.rooms.append((row,col))
        last_room = (row,col)
        self.start_room = last_room
        direction = random.randint(1,4)

        max_rooms = random.randint(MIN_ROOMS, MAX_ROOMS)
        while room_id < max_rooms:
            roll = random.random()
            if roll > 0.8:
                row, col = random.choice(self.rooms)
            else:
                row, col = last_room
            if roll > 0.3:
                (new_row,new_col,direction) = self.add_room(row,col,direction)
            else: 
                (new_row,new_col,direction) = self.add_room(row,col)
            if new_row >= 0:
                room_id += 1  
                self.level_map[new_row][new_col] = room_id
                self.rooms.append((new_row,new_col))
                last_room = (new_row,new_col)
            
        self.room_count = room_id

    def add_room(self,row,col,direction=0):
        if direction:
            n = direction
        else:
            n = random.randint(1,4)
        if n == 1:
            return self.add_room_north(row,col)
        elif n == 2:
            return self.add_room_south(row,col)
        elif n == 3:
            return self.add_room_east(row,col)
        else:
            return self.add_room_west(row,col)

    def add_room_north(self,row,col):
        if row+1 >= LEVEL_ROWS or self.level_map[row+1][col] > 0:
            return (-1,-1,1)
        else:
            return (row+1,col,1)
    
    def add_room_south(self,row,col):
        if row-1 <= 0 or self.level_map[row-1][col] > 0:
            return (-1,-1,2)
        else:
            return (row-1,col,2)

    def add_room_east(self,row,col):
        if col+1 >= LEVEL_COLS or self.level_map[row][col+1] > 0:
            return (-1,-1,3)
        else:
            return (row,col+1,3) 

    def add_room_west(self,row,col):
        if col-1 <= 0 or self.level_map[row][col-1] > 0:
            return (-1,-1,4)
        else:
            return (row,col-1,4)

    def show(self):
        for row in range(LEVEL_ROWS):
            for col in range(LEVEL_COLS):
                room = self.level_map[row][col]
                if room > 0:
                    print "%3d" % (room),
                else:
                    print "---",
            print

    def save(self):
        name = "../data/%d.level" % (self.id)
        fh = open(name, 'wb')
        if fh:
            pickle.dump(self, fh, 2)
            fh.close()

    def save_image(self):
        try:
            from PIL import Image, ImageDraw
        except:
            raise

        im = Image.new("RGB", (20*LEVEL_COLS,20*LEVEL_ROWS), "black")
        draw = ImageDraw.Draw(im)
        for row,col in self.rooms:
            x = col*20
            y = row*20
            draw.rectangle((x + 5, y + 5, x+15, y+15), fill="white")

        name = "../data/dungeon_%d.png" % (self.id)
        im.save(name, "PNG")
 
    def getsizeof(self):
        size = sys.getsizeof(self)
        return size

    def get_as_dict(self):
        self.level_dict["room_count"] = 0
        (row,col) = self.start_room
        self.level_dict["start_room"] = "%i,%i" % (row,col)
        for row in range(LEVEL_ROWS):
            for col in range(LEVEL_COLS):
                room = self.level_map[row][col]
                if room > 0:
                    self.level_dict["rooms"]["%i,%i" % (row,col)] = room 
                    self.level_dict["room_count"] += 1
        return self.level_dict

    def get_db(self):
        TEST_MODE = True
        try:
            conn = Connection('localhost', 27017)
        except ConnectionFailure:
            raise Exception("Unable to connect to database")
            return None

        if TEST_MODE:
            db = conn.test # test database
        else:
            db = conn.prd # production database

        return (conn, db)

    def save_dungeon_floor(self,floor,id):
        """
        """
        (conn, db) = self.get_db()

        if db:
            cursor = db.floors
            #log.info("get_player_info: Creating new player: fb_uid = " + uid + " name = " + name)
            floor["_id"] = id
            cursor.save(floor)

            #for i in result:
            #    log.info("get_player_info: " + i + " " + str(result[i]))

            return True
        else:
            #log.error("get_player_info: couldn't connect to db")
            return None

if __name__ == "__main__":
    random.seed()
    for i in range(499): 
        obj = Level(i)
        d = obj.get_as_dict()
        obj.save_dungeon_floor(d, i + 1)
        #obj.show()
        #print "sizeof level: %d bytes with %d rooms" % (obj.getsizeof(),obj.room_count)
        obj.save_image()
