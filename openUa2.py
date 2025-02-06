import asyncio
import myServer as s
from asyncua import Client, Node

async def run_open_ua(camera):
    """
    Main task of this Client-Subscription example.
    """
    client = Client(url=s.ip)
    async with client:
        handler = SubscriptionHandler(camera, client)
        subscription = await client.create_subscription(50, handler)
        nodes = [
            client.get_node(s.current_layer),
            client.get_node(s.job_file),
            client.get_node(s.scan_command),
            client.get_node(s.SF0_Field_DataBlockInfo),
            client.get_node(s.scan_status)
        ]
        await subscription.subscribe_data_change(nodes)
        while subscription:
            await asyncio.sleep(5)
        await subscription.delete()
        await asyncio.sleep(1)


class SubscriptionHandler:
    def __init__(self, camera, client):
        self.camera = camera
        self.previous_status = 7

    def datachange_notification(self, node: Node, val, data):
        if str(node) == s.scan_status:
            self.status_change(val)

    def status_change(self, val):
        if val == 1:
            print("Opening Job File")
        elif val == 7 and self.previous_status != 7:
            print("Scan Complete")
            self.camera.stop_acquiring()
        self.previous_status = val
