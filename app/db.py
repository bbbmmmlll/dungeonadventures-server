"""
All database access uses this module.
"""
import pymongo
from pymongo import Connection
from pymongo.errors import ConnectionFailure
import random
import time
import datetime

import app.config
from app.log import mylogger as log


def get_db():
    try:
        conn = Connection('localhost', 27017) 
    except ConnectionFailure:
        raise Exception("Unable to connect to database")
        log.error("Unable to connect to database")
        return None

    if app.config.TEST_MODE:
        db = conn.test # test database
    else:
        db = conn.prd # production database

    return (conn, db)


def test_database():
    """
    """
    (conn, db) = get_db() 

    if db:
        log.info("Database version: " + conn.server_info()['version'])
        return True
    else:
        log.error("test_database: couldn't connect to db")
        return False   


def get_player_info(uid, name, pic_square):
    """
    """
    (conn, db) = get_db() 

    if db:
        cursor = db.players
        result = cursor.find_one({"fb_uid": uid})
        log.info("get_player_info: find_one by fb_uid, uid = " + uid)
        ts = time.time()
        if result == None:
            # new player, create record
            log.info("get_player_info: Creating new player: fb_uid = " + uid + " name = " + name)
            player = {"fb_uid": uid,
                      "name" : name,
                      "pic_square" : pic_square,
                      "xp": 0,
                      "gold": 0,
                      "level": 1,
                      "sp": 5,
                      "max_sp": 5,
                      "attack": 0,
                      "defense": 0,
                      "hp": 20,
                      "max_hp": 20,
                      "actions": 0,
                      "errors": 0,
                      "dungeon_id": 0, # for now zero = in town
                      "result_id": 0,
                      "result_msg": "",
                      "dungeon_coord": None,
                      "monster_id": 1, # dummy
                      "monster_hp": 100, # dummy
                      "north": 0,
                      "south": 0,
                      "east": 0,
                      "west": 0,
                      "trap_id": 0,
                      "chest_id": 0,
                      "stairs": 0,
                      "session_id": 1919, # dummy
                      "timestamp": ts,
                      "created": ts,
                      "version": 1,
                     }
            cursor.save(player)
            result = cursor.find_one({"fb_uid": uid}) # make sure it was created
            add_news(uid, ts, pic_square, "%s created a character at %s" % (player["name"], datetime.datetime.now()))
        else:
            log.info("get_player_info: Found player: fb_uid = " + uid + " name = " + name)
            if result["timestamp"] < ts - 3600:
                add_news(uid, ts, pic_square, "%s logged on at %s" % (result["name"], datetime.datetime.now()))

        for i in result:
           log.info("get_player_info: " + i + " " + str(result[i]))

        return result
    else:
        log.error("get_player_info: couldn't connect to db")
        return None


def do_attack(uid):
    """
    """
    (conn, db) = get_db()

    if db:
        cursor = db.players
        player = cursor.find_one({"fb_uid": uid})
        log.info("do_attack: fb_uid = " + uid)
        if player == None:
            log.info("do_attack: player: fb_uid = " + uid + "not found")
            return None
        elif player["monster_id"] < 1:
            log.info("do_attack: player: fb_uid = " + uid + " found nothing to attack ")
            return player
        else:
            log.info("do_attack: player: fb_uid = %s attacks mon_id = %d " % (uid, player["monster_id"]))
            i = random.randint(1,100)
            if i > 30: # dummy hit
                mon_hp = player["monster_hp"]
                mon_hp -= random.randint(2,20) 
                if mon_hp < 1:
                    log.info("do_attack: player: fb_uid = %s kills mon_id = %d " % (uid, player["monster_id"]))
                    player["monster_id"] = 0
                    player["monster_hp"] = 0
                    player["xp"] += 1
                    player["gold"] += random.randint(2,20)
                else:
                    log.info("do_attack: player: fb_uid = %s hits mon_id = %d " % (uid, player["monster_id"]))
                    player["monster_hp"] = mon_hp 
                player["timestamp"] = time.time()
                cursor.save(player)
            else: #miss
                log.info("do_attack: player: fb_uid = %s misses mon_id = %d " % (uid, player["monster_id"]))
                player["timestamp"] = time.time()
                cursor.save(player)
             
        return player #is this needed?
    else:
        log.error("do_attack: couldn't connect to db")
        return None

def get_news(uid):
    """Get news for this player"""
    (conn, db) = get_db()

    if db:
        news_cursor = db.news
        # TODO: probably uses too many resources
        news = news_cursor.find({}, {"Image":1,"Item":1}).sort("ts", pymongo.DESCENDING).limit(15); # 15 results maximum
        result = [] 
        for items in news:
            result.append(items)
            log.info("get_news: %s" % (items["Item"]))
        return result
    else:
        log.error("get_news: couldn't connect to db")
        return None

def add_news(uid,ts,image,item):
    """Add news"""
    (conn, db) = get_db()

    if db:
        news_cursor = db.news
        news = {"uid": uid, "ts": ts, "Image": image, "Item": item}
        news_cursor.save(news)
    else:
        log.error("add_news: couldn't connect to db")
        return None

def get_quests(uid):
    pass

def get_friends(uid):
    pass

def get_inventory(uid):
    pass

def do_move(uid, direction):
    """Move between rooms in a dungeon"""
    if direction not in ("n","s","e","w","u","d"):
        return None

    (conn, db) = get_db()

    if db:
        player_cursor = db.players 
        player = player_cursor.find_one({"fb_uid" : uid})
        floor_cursor = db.floors
        # TODO: test if found or not
        floor  = floor_cursor.find_one({"_id" : player["dungeon_id"]})
        (row,col) = player["dungeon_coord"].split(",")
        try_row = int(row)
        try_col = int(col)

        if direction == "d":
            if player["dungeon_coord"] in floor["exits"]:
                log.info("do_move: found exit")
                return None
        elif direction == "u":
            return None

        if direction == "n":
            try_row += 1            
        elif direction == "s":
            try_row -= 1            
        elif direction == "e":
            try_col += 1
        else: 
            try_col -= 1

        try_coord = "%i,%i" % (try_row,try_col)
        if floor["rooms"][try_coord]:
            player["dungeon_coord"] =  try_coord
            player_cursor.save(player)
            log.info("do_move: moved from %s,%s to %i,%i" % (row,col,try_row,try_col))

    else:
        log.error("do_move: couldn't connect to db")
        return None
   
def use_item(uid):
    pass

def consume_item(uid):
    pass

def cast_spell(uid):
    pass

def get_store_items(uid):
    pass

def get_floor(uid):
    """Get a new dungeon floor for a player and move them to it"""
    (conn, db) = get_db()

    if db:
        cursor = db.floors
        result = cursor.find().count()
        log.info("get_floor: found %i floors" % (result))
        if result > 0:
            f = random.randint(1, result - 1)
            floor  = cursor.find_one({"_id" : f})
            # TODO: test if found or not
            cursor = db.players 
            player = cursor.find_one({"fb_uid" : uid})
            # TODO: test if found or not
            player["dungeon_id"] = f
            player["dungeon_coord"] = floor["start_room"]
            log.info("get_floor: uid = %s got dungeon = %i dungeon_coord = %s" % (uid,f,floor["start_room"]))

            # TODO: this is not very efficent    
            rooms = floor["rooms"]
            (row,col) = player["dungeon_coord"].split(",")
            try_row = int(row)
            try_col = int(col)
            for key in rooms:
                log.info("found: %s" % key)
            try_coord = "%i,%i" % (try_row+1,try_col)
            log.info("get_floor: uid = %s try_coord = %s" % (uid,try_coord))
            if try_coord in rooms:
                player["north"] = try_coord
            else:
                player["north"] = ""
            try_coord = "%i,%i" % (try_row-1,try_col)
	    log.info("get_floor: uid = %s try_coord = %s" % (uid,try_coord))
            if try_coord in rooms:
                player["south"] = try_coord
            else:
                player["south"] = ""
            try_coord = "%i,%i" % (try_row,try_col+1)
            log.info("get_floor: uid = %s try_coord = %s" % (uid,try_coord))
            if try_coord in rooms:
                player["east"] = try_coord
            else:
                player["east"] = ""
            try_coord = "%i,%i" % (try_row,try_col-1)
            log.info("get_floor: uid = %s try_coord = %s" % (uid,try_coord))
            if try_coord in rooms:
                player["west"] = try_coord
            else:
                player["west"] = ""

            cursor.save(player)
            return player
        else:
            return None
    else:
        log.error("get_floor: couldn't connect to db")
        return None

# This is for testing only, remove for production
def get_monster(uid):
    """Get a new monster for a player"""
    (conn, db) = get_db()

    if db:
        cursor = db.floors
        result = cursor.find().count()
        log.info("get_monster: found %i monsters" % (result))
        if result > 0:
            id = random.randint(1, result - 1)
            floor  = cursor.find_one({"_id" : id})
            # TODO: test if found or not
            cursor = db.players
            player = cursor.find_one({"fb_uid" : uid})
            # TODO: test if found or not
            # we need to make a monster table!
            player["monster_id"] = id
            player["monster_hp"] = random.randint(10,50)
            log.info("get_monster: uid = %s got monster = %i" % (uid,id))
            cursor.save(player)
            return player
        else:
            return None
    else:
        log.error("get_monster: couldn't connect to db")
        return None

def delete_player(uid, session_id):
    pass

