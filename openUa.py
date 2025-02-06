import os
import asyncio
import logging
import myServer as s
from asyncua import Client, Node, ua
import time
async def run_open_ua(camera):
    """
    Main task of this Client-Subscription example.
    """
    client = Client(url=s.ip )
    async with client:
        handler = SubscriptionHandler(camera,client)
        # We create a Client Subscription.
        subscription = await client.create_subscription(50, handler)
        nodes = [
            client.get_node(s.current_layer),
            client.get_node(s.job_file),
            client.get_node(s.scan_command),
            client.get_node(s.SF0_Field_DataBlockInfo),
            client.get_node(s.scan_status)

        ]
        # We subscribe to data changes for two nodes (variables).
        await subscription.subscribe_data_change(nodes)
        # We let the subscription run for ten seconds
        while subscription != None:
            await asyncio.sleep(5)        # We delete the subscription (this un-subscribes from the data changes of the two variables).
        # This is optional since closing the connection will also delete all subscriptions.
        await subscription.delete()
        # After one second we exit the Client context manager - this will close the connection.
        await asyncio.sleep(1) 

class SubscriptionHandler:
    def __init__(self,camera,client):
        self.current_status = 0
        self.Job_File = ""
        self.layer = 0
        self.OutputDirectory = "IMAGE_DIRECTORY"
        self.OutputPath = ""
        self.camera = camera
        self.previous_status = 7
        print(f"previous node {self.previous_status}")
    """
    The SubscriptionHandler is used to handle the data that is received for the subscription.
    """
    def datachange_notification(self, node: Node, val, data):
        if str(node) == s.current_layer:
            self.layer_change(val)
        if str(node) == s.job_file:
            print("Job File Changed to ", val)
            if val != None and val !="" and val !="\n":
                self.JobFile_change(val)
                return
            else:
                print("Job File is Empty")
                return
        if str(node) == s.scan_status:   
            self.status_change(val)
        if str(node) == s.scan_command:   
            self.command_change(val)
        if str(node) == s.SF0_Field_DataBlockInfo:   
            self.data_info(val)
    def JobFile_change(self, val):
        #New Job File
        # Check if directory exists and create it if necessary
        print("Job File Change function")
        self.Job_File = os.path.basename(val)
        self.OutputPath = os.path.join(self.OutputDirectory, self.Job_File)
        self.Powder_OutputPath = os.path.join(self.OutputPath,"PowderBedImages")
        self.Layer_OutputPath = os.path.join(self.OutputPath,"LayerImages")
        if not os.path.exists(self.OutputPath):
            print("Directory Created")
            os.makedirs(self.OutputPath)
            os.makedirs(self.Powder_OutputPath)
            os.makedirs(self.Layer_OutputPath)
        pass
    def layer_change(self, val):
        self.layer = val
        pass
    def status_change(self, val):
        print(val)
        if val == 1:
            #Openning Job File
            print("Openning Job File")
        
        elif val == 7 and self.previous_status != 7:
            ##################IMPORTANT PARAMETERS FOR TIMING#######################      
            #Scan Complete
            print("ScanComplete")
            self.camera.stop_acquiring()  
        self.previous_status = val
        
    def command_change(self, val):
        print(val)
        if val == 3 :
            self.camera.start_aquiring()
            print(f'recording')
    def data_info(self, val):
        pass