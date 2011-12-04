#!/usr/bin/python
import pyamf
from pyamf.remoting.client import RemotingService

client = RemotingService('http://localhost:8000/amf')
service = client.getService('DAService')

