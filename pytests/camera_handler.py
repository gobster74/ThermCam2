from pytests.camera import Camera
import os
import time
import numpy as np
import csv

class CameraHandler:
    def __init__(self, log_dir='.', config_csv='data_blocks.csv'):
        self.log_dir = log_dir
        self.config_csv = config_csv
        self.cameras = {}
        self.cameras['PI 1M'] = Camera('PI 1M', log_dir)
        self.cameras['PI 640i'] = Camera('PI 640i', log_dir)
        
        self.load_data_block_csv()

    def load_data_block_csv(self):
        """Loads the CSV for data block index and position info."""
        self.data_blocks = {}

        with open(self.config_csv, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    data_block_id, x, y = row
                    self.data_blocks[int(data_block_id)] = {'x': int(x), 'y': int(y)}

    def start_recording(self):
        """Start recording on both cameras."""
        for camera in self.cameras.values():
            camera.start_aquiring()

    def stop_recording(self):
        """Stop recording on both cameras."""
        for camera in self.cameras.values():
            camera.stop_acquiring()

    def send_data_block_index(self, data_block_index):
        """Send the data block index to both cameras."""
        if data_block_index in self.data_blocks:
            positions = self.data_blocks[data_block_index]
            print(f"Sending DataBlock {data_block_index} to cameras with position: {positions}")
            # Update the position for both cameras based on the data block index
            self.cameras['PI 1M'].change_roi(x=positions['x'], y=positions['y'])
            self.cameras['PI 640i'].change_roi(x=positions['x'], y=positions['y'])
        else:
            print(f"DataBlock {data_block_index} not found in CSV.")
