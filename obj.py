import ctypes
import os
import time
import pyOptris as optris
import numpy as np
import multiprocessing

camera_id = {
    'PI 1M': '17092037.xml', 
    'PI 640i': '6060300.xml',
}

class Camera:
    def __init__(self, name, log_dir='.', csv_file='data_blocks.csv'):
        self.name = name
        self.log_dir = log_dir
        self.csv_file = csv_file

    def start_acquiring(self):
        print(f"{self.name} started acquiring.")

    def stop_acquiring(self):
        print(f"{self.name} stopped acquiring.")

    def update_position(self, index):
        print(f"{self.name} updated position to index {index}")

class CameraHandler:
    def __init__(self, log_dir='.', csv_file='data_blocks.csv'):
        self.command_queue_1m = multiprocessing.Queue()
        self.command_queue_640 = multiprocessing.Queue()

        # process for each camera
        self.process_1m = multiprocessing.Process(target=self.run_camera, args=("PI 1M", log_dir, csv_file, self.command_queue_1m))
        self.process_640 = multiprocessing.Process(target=self.run_camera, args=("PI 640i", log_dir, csv_file, self.command_queue_640))

    @staticmethod
    def run_camera(name, log_dir, csv_file, command_queue):
        """Function to run each camera in a separate process."""
        camera = Camera(name, log_dir, csv_file)
        while True:
            command = command_queue.get()
            if command == "start":
                camera.start_acquiring()
            elif command == "stop":
                camera.stop_acquiring()
            elif isinstance(command, int):  # if it's an integer, assume it's a data block index
                camera.update_position(command)
            elif command == "exit":
                break  # quite loop 

    def start_cameras(self):
        """Start the camera processes and begin acquiring images."""
        self.process_1m.start()
        self.process_640.start()
        self.command_queue_1m.put("start")
        self.command_queue_640.put("start")

    def stop_cameras(self):
        """Stop the cameras and terminate processes."""
        self.command_queue_1m.put("stop")
        self.command_queue_640.put("stop")
        self.command_queue_1m.put("exit")
        self.command_queue_640.put("exit")

        self.process_1m.join()
        self.process_640.join()

    def send_data_block_index(self, index):
        """Send data block index to both camera processes."""
        self.command_queue_1m.put(index)
        self.command_queue_640.put(index)
