import os
import asyncio
import logging
import myServer as s
from asyncua import Client, Node
import time

class SubscriptionHandler:
    def __init__(self, camera_handler, client):
        self.camera_handler = camera_handler  
        self.client = client
        self.current_status = 0
        self.Job_File = ""
        self.layer = 0
        self.OutputDirectory = "IMAGE_DIRECTORY"
        self.OutputPath = ""
        self.previous_status = 7
        print(f"previous node {self.previous_status}")

    def datachange_notification(self, node: Node, val, data):
        """Handles incoming OPC UA data changes."""
        if str(node) == s.current_layer:
            self.layer_change(val)
        elif str(node) == s.job_file:
            self.job_file_change(val)
        elif str(node) == s.scan_status:   
            self.status_change(val)
        elif str(node) == s.scan_command:   
            self.command_change(val)
        elif str(node) == s.SF0_Field_DataBlockInfo:   
            self.data_info(val)

    def job_file_change(self, val):
        """Handles job file updates."""
        if val and val.strip():
            self.Job_File = os.path.basename(val)
            self.OutputPath = os.path.join(self.OutputDirectory, self.Job_File)
            self.Powder_OutputPath = os.path.join(self.OutputPath, "PowderBedImages")
            self.Layer_OutputPath = os.path.join(self.OutputPath, "LayerImages")

            os.makedirs(self.OutputPath, exist_ok=True)
            os.makedirs(self.Powder_OutputPath, exist_ok=True)
            os.makedirs(self.Layer_OutputPath, exist_ok=True)
            
            print(f"Job File Updated: {self.Job_File}")

    def layer_change(self, val):
        """Handles layer changes (can be used for tracking)."""
        self.layer = val

    def status_change(self, val):
        """Handles status changes and starts/stops cameras accordingly."""
        print(f"Status Changed: {val}")
        
        if val == 1:
            print("Opening Job File")
        
        elif val == 7 and self.previous_status != 7:
            print("Scan Complete, stopping cameras")
            self.camera_handler.stop_cameras()

        self.previous_status = val

    def command_change(self, val):
        """Handles scan commands and starts recording."""
        print(f"Command Received: {val}")
        
        if val == 3:
            print("Starting recording on both cameras")
            self.camera_handler.start_cameras()

    def data_info(self, val):
        """Handles data block updates and moves cameras accordingly."""
        try:
            block_id = int(val)
            print(f"New Data Block ID Received: {block_id}")
            self.camera_handler.send_datablock(block_id)
        except ValueError:
            print(f"Invalid data block ID received: {val}")

async def run_open_ua(camera_handler):
    """
    Connects to the OPC UA server and listens for data changes.
    """
    client = Client(url=s.ip)
    
    async with client:
        handler = SubscriptionHandler(camera_handler, client)
        subscription = await client.create_subscription(50, handler)

        nodes = [
            client.get_node(s.current_layer),
            client.get_node(s.job_file),
            client.get_node(s.scan_command),
            client.get_node(s.SF0_Field_DataBlockInfo),
            client.get_node(s.scan_status),
        ]
        await subscription.subscribe_data_change(nodes)

        while True:
            await asyncio.sleep(5) 

        await subscription.delete()
        await asyncio.sleep(1)
