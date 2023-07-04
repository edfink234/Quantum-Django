import json
from asgiref.sync import async_to_sync
import channels.layers

def broadcast_ticks(ticks):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.TICKS_GROUP_NAME, {
            "type": 'new_ticks',
            "content": json.dumps(ticks),
        })

ticks = [
    {'symbol': 'BTCUSDT', 'lastPrice': 1234, },
]
broadcast_ticks(ticks)