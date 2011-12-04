import random

import app.db
import app.utils
import app.config
from app.log import mylogger as log

class Controller(object):
    def get_player_info(self, uid, name, pic_square):
        log.info("controller: called get_player_info uid = " + uid + " " + name)
        return app.db.get_player_info(uid, name, pic_square)

    def do_move(self, uid, direction):
        log.info("controller: called do_move uid = %s, d = %s" % (uid, direction))
        return app.db.do_move(uid, direction) 

    def do_attack(self, uid):
        log.info("controller: called do_attack uid = " + uid)
        return app.db.do_attack(uid) 

    def get_news(self, uid):
        log.info("controller: called get_news uid = " + uid)
        return app.db.get_news(uid)

    def get_floor(self, uid):
        log.info("controller: called get_floor uid = " + uid)
        return app.db.get_floor(uid)

    def get_monster(self, uid):
        log.info("controller: called get_monster uid = " + uid)
        return app.db.get_monster(uid)

    def raiseException(self):
        raise Exception("No controller action found")
