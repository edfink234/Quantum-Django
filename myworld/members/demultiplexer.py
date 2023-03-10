from channels_demultiplexer.demultiplexer import WebsocketDemultiplexer

from .consumers import ZMQChannels

class Demultiplexer(WebsocketDemultiplexer):
    # Wire your async JSON consumers here: {stream_name: consumer}
    consumer_classes = {
        "echo": ZMQChannels,
    }
