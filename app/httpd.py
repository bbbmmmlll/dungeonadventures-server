"""
Embedded web server.
"""
import os.path, os
import gevent
from gevent import wsgi

import amfast
from amfast.remoting.wsgi_channel import WsgiChannelSet, WsgiChannel

import app.utils
import app.config
from app.log import mylogger as log

class WebServer(object):
    """
    Start embedded web server.
    """
    def __init__(self):
        #self.setDaemon(True)
        #self.setName('WebServer')
        
        channel_set = WsgiChannelSet()
        rpc_channel = WsgiChannel('amf')
        channel_set.mapChannel(rpc_channel)
        app.utils.setup_channel_set(channel_set)

        try:
            log.info('Listening for connections')
            server = wsgi.WSGIServer(('', 8000), channel_set).serve_forever()
            server.handler_class(channel_set)
         
        except (KeyboardInterrupt, SystemExit):
            raise

        return None
