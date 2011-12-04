"""Utility functions."""
import sys

import amfast
from amfast.encoder import Encoder
from amfast.decoder import Decoder
from amfast.remoting import Service, CallableTarget

from app.log import mylogger as log
import app.controller

def setup_channel_set(channel_set):
    """Configures an amfast.remoting.channel.ChannelSet object."""

    #amfast.logger = log.logger

    # Map service targets to controller methods
    cont_obj = app.controller.Controller()
    service = Service('DAService')
    service.mapTarget(CallableTarget(cont_obj.get_player_info, 'get_player_info'))
    service.mapTarget(CallableTarget(cont_obj.do_move, 'do_move'))
    service.mapTarget(CallableTarget(cont_obj.do_attack, 'do_attack'))
    service.mapTarget(CallableTarget(cont_obj.get_news, 'get_news'))
    service.mapTarget(CallableTarget(cont_obj.get_floor, 'get_floor'))
    service.mapTarget(CallableTarget(cont_obj.get_monster, 'get_monster'))
    service.mapTarget(CallableTarget(cont_obj.raiseException, 'raiseException'))
    channel_set.service_mapper.mapService(service)
