#!/usr/bin/env python
"""
Main module for dad.

Start threads.
"""
import sys
import time
import datetime

from app.log import mylogger as log
from app.daemon import Daemon
import app.config
import app.timer
import app.config
import app.timer
import app.db
import app.httpd
import app.worker

PROGNAME = 'dad'
VERSION = '0.0.13'

log.info(PROGNAME + ' version ' + VERSION + ' starting')

class MyDaemon(Daemon):
    def run(self):

        log.info('Starting Database: ')
        DB = app.db.test_database()
        if DB:
            log.info('Database started')
        else:
            log.critical('Database failed to initalize - aborting')
            sys.exit(1)

        app.db.add_news(0, time.time(), "http://da.mithrilsoft.com/da/assets/images/logo_50x50.gif", "Server version %s was restarted at %s" % (VERSION, datetime.datetime.now()))

        log.info('Starting Webserver: ')
        try:
            WS = app.httpd.WebServer()
            log.info('Webserver started')
        except:
            log.critical('Webserver failed to initalize - aborting')
            sys.exit(1)

        #log.info('Starting Timer: ')
        #TM = app.timer.Timer()
        #if TM:
        #    log.info('Timer started')
        #else:
        #    log.critical('Timer failed to initalize - aborting')
        #    sys.exit(1)

        #with daemon.DaemonContext():
        # do nothing useful for now                  
        while True:
            log.info('waking up')
            time.sleep(600)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/dad.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'startforeground' == sys.argv[1]:
            daemon.startforeground()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|startforeground" % sys.argv[0]
        sys.exit(2)
