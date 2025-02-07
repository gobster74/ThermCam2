import os
import time
import numpy as np
import pyOptris as optris
from typing import Tuple

camera_id = {
    'PI 1M': '17092037.xml', 
    'PI 640i': '6060300.xml',
}

class Camera:
    def __init__(self, type: str, log_dir: str = '.'):
        self.type = type
        self.log_dir = log_dir
        self.is_recording = False
        self.max_buffer_size = 12500 
        self.camera_id = None
        self.frames_counter = 0
        self.frame_buffer = np.empty((self.max_buffer_size, 0, 0), dtype=np.uint16)
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.log_file = os.path.join(self.log_dir, f"log_{self.type}_{int(time.time())}.log")
        print(f"saving log at: {self.log_file}")
        
        self.initialize_camera()
        
    def initialize_camera(self):
        print(f"Initializing {self.type} camera...")
        config_file = camera_id.get(self.type)
        if not config_file:
            raise ValueError("invalid camera type")
        
        config_file_path = os.path.abspath(config_file)
        if not os.path.exists(config_file_path):
            print(f"Configuration file not found: {config_file_path}")
            return

        err, self.camera_id = optris.multi_usb_init(config_file, None, self.log_file)
        if err != 0:
            print(f"Failed to initialize {self.type}: error Code {err}")
            self.camera_id = None
        else:
            self.camera_id = self.camera_id.value
            serial = optris.get_multi_get_serial(self.camera_id)
            print(f"{self.type} camera initialized successfully. Camera serial: {serial}")
            self.w, self.h, err = optris.get_multi_thermal_image_size(self.camera_id)
        
    def start_acquiring(self):
        if not self.camera_id:
            print(f"Error starting the camera")
            return 
        self.is_recording = True
        print(f"Starting recording for {self.type}")
    
    def acquire_frames(self):
        if self.is_recording:
            if not self.camera_id:
                print("Camera did not start, no frames are being saved.")
                return
            print(f"Acquiring frames for {self.type}...")
            self.frames_counter = 0

            try:
                start_time = time.time()
                while self.is_recording:
                    frame, err = optris.get_multi_thermal_image(self.camera_id, self.w, self.h)
                    if int(err) == 0:
                        self.frame_buffer[self.frames_counter] = np.frombuffer(frame, dtype=np.uint16).reshape(self.h, self.w)
                        self.frames_counter += 1
                        if self.frames_counter == self.max_buffer_size:
                            print(f"Buffer full, {self.max_buffer_size} frames acquired.")
                            self.stop_acquiring()
                            self.change_roi(x=np.random.randint(0, 400), y=np.random.randint(0, 300))
                    else:
                        print(f"Error acquiring frame: {err}")
            except Exception as e:
                print(f"Error during frame acquisition: {e}")
            print(f"Stopping recording, last frame acquired: {self.frames_counter}")

    def stop_acquiring(self, save_dir='frames'):
        if self.is_recording:
            self.is_recording = False
            self.save_buffer(save_dir)
            self.frame_buffer = np.empty((self.max_buffer_size, self.h, self.w), dtype=np.uint16)
            print("Recording stopped and frames saved.")

    def save_buffer(self, save_dir="frames"):
        os.makedirs(save_dir, exist_ok=True)
        timestamp = int(time.time())
        filename = os.path.join(save_dir, f"frames_{self.camera_id}_{timestamp}.npy")
        np.save(filename, self.frame_buffer[:self.frames_counter])
        print(f"Saved buffer to {filename}")

    def change_roi(self, x=None, y=None):
        self.position = optris.set_multi_clipped_format_position(self.camera_id, x, y)
