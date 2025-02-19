import os
import asyncio
import logging
import myServer as s
from asyncua import Client, Node, ua
import time

async def run_open_ua(camera_handler, command_queue):
    client = Client(url=s.ip)
    async with client:
        handler = SubscriptionHandler(camera_handler, client)
        subscription = await client.create_subscription(50, handler)

        # Subscribe to data changes
        nodes = [
            client.get_node(s.current_layer),
            client.get_node(s.job_file),
            client.get_node(s.scan_command),
            client.get_node(s.SF0_Field_DataBlockInfo),
            client.get_node(s.scan_status)
        ]
        await subscription.subscribe_data_change(nodes)

        while subscription:
            await asyncio.sleep(1)

        await subscription.delete()
        await asyncio.sleep(1)

class SubscriptionHandler:
    def __init__(self, camera_handler, client):
        self.current_status = 0
        self.Job_File = ""
        self.layer = 0
        self.OutputDirectory = "IMAGE_DIRECTORY"
        self.OutputPath = ""
        self.camera_handler = camera_handler 
        self.previous_status = 7
        print(f"Previous node {self.previous_status}")

    """
    The SubscriptionHandler is used to handle the data that is received for the subscription.
    """
    def datachange_notification(self, node: Node, val, data):
        if str(node) == s.current_layer:
            self.layer_change(val)
        elif str(node) == s.job_file:
            print("Job File Changed to ", val)
            if val and val.strip():  # checks if value is not empty
                self.JobFile_change(val)
            else:
                print("Job File is Empty")
        elif str(node) == s.scan_status:   
            self.status_change(val)
        elif str(node) == s.scan_command:   
            self.command_change(val)
        elif str(node) == s.SF0_Field_DataBlockInfo:   
            self.data_info(val)

    def JobFile_change(self, val):
        print("Job File Change detected")
        self.Job_File = os.path.basename(val)
        self.OutputPath = os.path.join(self.OutputDirectory, self.Job_File)
        self.Powder_OutputPath = os.path.join(self.OutputPath, "PowderBedImages")
        self.Layer_OutputPath = os.path.join(self.OutputPath, "LayerImages")

        if not os.path.exists(self.OutputPath):
            print("Creating job directories")
            os.makedirs(self.OutputPath)
            os.makedirs(self.Powder_OutputPath)
            os.makedirs(self.Layer_OutputPath)

        # notifies CameraHandler of job file change
        print(f"New job file set: {self.Job_File}")

    def layer_change(self, val):
        self.layer = val

    def status_change(self, val):
        print(val)
        if val == 1:
            # opening Job File
            print("Opening Job File")
        elif val == 7 and self.previous_status != 7:
            # scan Complete
            print("Scan Complete")
            self.camera_handler.stop_cameras()  # stop both cameras
        self.previous_status = val
        
    def command_change(self, val):
        print(val)
        if val == 3:
            self.camera_handler.start_cameras()  # start both cameras
            print("Recording started")

    def data_info(self, val):
        pass