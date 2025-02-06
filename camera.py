import time
import numpy as np
import os
import csv
import pyOptris as optris

camera_id = {
    'PI 1M': '17092037.xml', 
    'PI 640i': '6060300.xml',
}
log_dir = '.'

class Camera:
    def __init__(self, type, log_dir='.', config_csv='data_blocks.csv'):
        self.type = type
        self.log_dir = log_dir
        self.config_csv = config_csv
        self.is_recording = False
        self.max_buffer_size = 12500
        self.camera_id = None
        self.frames_counter = 0
        self.frame_buffer = np.empty((self.max_buffer_size, 96, 96), dtype=np.uint16)
        self.data_blocks = self.load_data_blocks()
        self.current_position = None
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = os.path.join(self.log_dir, f"log_{self.type}_{int(time.time())}.log")
        print(f"saving log at: {self.log_file}")
        self.initialize_camera()
        
    def load_data_blocks(self):
        data_blocks = {}
        if os.path.exists(self.config_csv):
            with open(self.config_csv, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data_blocks[row[0]] = {'x': int(row[1]), 'y': int(row[2])}
        return data_blocks

    def initialize_camera(self): 
        print(f"Initializing {self.type} camera...")
        config_file = camera_id.get(self.type)
        if not config_file:
            raise ValueError("invalid camera type")
        
        config_file_path = os.path.abspath(config_file)
        if not os.path.exists(config_file_path):
            print(f"Configuration file not found: {config_file_path}")
            return

        err, self.camera_id = optris.multi_usb_init(
            config_file, None, self.log_file
        )

        if err != 0:
            print(f"failed to initialize {self.type}: error Code {err}")
            self.camera_id = None
        else:
            self.camera_id = self.camera_id.value 
            serial = optris.get_multi_get_serial(self.camera_id)
            print(f"{self.type} camera initialized successfully. camera serial: {serial}")
            self.w, self.h, err = optris.get_multi_thermal_image_size(self.camera_id)
        
        # PI 1M
        #err,ID1 = optris.multi_usb_init(camera_id[type],None, os.path.join(log_dir, f'log_1m_{int(time.time())}.log'))
        #if err != 0:
            #print(f"Failed to initialize PI 1M: {err}")
            #return False, None, None, None, None
        #print(f"{type} Serial: {optris.get_multi_get_serial(ID1)}")
        
    def start_aquiring(self):
        if not self.camera_id:
            print(f'error starting the camera')
            return 
        self.is_recording = True
        print(f'starting record')

    def aquire_frames(self):
        if self.is_recording:
            print(f'starting getting frames')
            self.frames_counter = 0
            try:
                start_time = time.time()
                while self.is_recording:
                    frame, err = optris.get_multi_thermal_image(self.camera_id, self.w, self.h)
                    if int(err) == 0:
                        timestamp = time.time()  # capture timestamp when frame is recorded
                        self.frame_buffer[self.frames_counter] = np.frombuffer(frame, dtype=np.uint16).reshape(self.h, self.w)
                        self.frames_counter += 1
                        print(f"Frame {self.frames_counter} recorded at {timestamp}")
            except Exception as e:
                print(f"Error: {e}")

    def stop_acquiring(self, save_dir='frames'):
        if self.is_recording:
            self.is_recording = False
            self.save_buffer(save_dir)
            print("recording stopped and frames saved")

    def save_buffer(self, save_dir="frames"):
        os.makedirs(save_dir, exist_ok=True)
        timestamp = int(time.time())
        filename = os.path.join(save_dir, f"frames_{self.camera_id}_{timestamp}.npy")
        np.save(filename, self.frame_buffer[:self.frames_counter])
        print(f"Saved buffer to {filename}")

    def change_roi(self, x, y):
        self.current_position = {'x': x, 'y': y}
        print(f"Changing ROI for {self.type} camera to {self.current_position}")
