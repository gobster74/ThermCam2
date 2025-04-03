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
    def __init__(self, name, log_dir='.', max_buffer_size=12500):
        self.name = name
        self.log_dir = log_dir
        self.is_recording = False
        self.max_buffer_size = max_buffer_size
        self.frames_counter = 0
        self.camera_id = None
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.log_file = os.path.join(log_dir, f"log_{self.name}_{int(time.time())}.log")
        print(f"Saving log at: {self.log_file}")
        
        self.initialize_camera()
        self.frame_buffer = np.empty((self.max_buffer_size, self.h, self.w), dtype=np.uint16)

    def initialize_camera(self):
        print(f"Initializing {self.name} camera...")
        config_file = camera_id.get(self.name)
        if not config_file:
            raise ValueError("Invalid camera type")
        
        err, self.camera_id = optris.multi_usb_init(config_file, None, self.log_file)
        if err != 0:
            print(f"Failed to initialize {self.name}: error code {err}")
            self.camera_id = None
        else:
            self.camera_id = self.camera_id.value
            serial = optris.get_multi_get_serial(self.camera_id)
            print(f"{self.name} camera initialized successfully. Serial: {serial}")
            self.w, self.h, err = optris.get_multi_thermal_image_size(self.camera_id)

    def start_acquiring(self):
        if not self.camera_id:
            print(f"Error starting the {self.name} camera")
            return
        self.is_recording = True
        print(f"{self.name} started acquiring.")

    def  acquire_frames(self):
        print(f"[DEBUG]  acquiree_frames() called, is_recording: {self.is_recording}")
        if not self.is_recording:
            print("[ERROR]  acquire_frames() called without start command!")
            return  
        self.frames_counter = 0
        start_time = time.time()
        try:
            while self.is_recording:
                frame, err = optris.get_multi_thermal_image(self.camera_id, self.w, self.h)
                if err == 0:
                    self.frame_buffer[self.frames_counter] = np.frombuffer(frame, dtype=np.uint16).reshape(self.h, self.w)
                    self.frames_counter += 1

                    if self.frames_counter == self.max_buffer_size:
                        print(f"{self.max_buffer_size / (time.time() - start_time)} FPS")
                        self.stop_acquiring()
                else:
                    print(f"Error {err}")
        except Exception as e:
            print(f"Error in {self.name}: {e}")

    def stop_acquiring(self):
        if self.is_recording:
            self.is_recording = False
            self.save_buffer()
            self.frame_buffer = np.empty((self.max_buffer_size, self.h, self.w), dtype=np.uint16)
            print(f"{self.name} stopped acquiring.")

    def save_buffer(self):
        #unique directory for each camera
        save_dir = os.path.join("frames", self.name)
        os.makedirs(save_dir, exist_ok=True)
        
        timestamp = int(time.time())
        filename = os.path.join(save_dir, f"frames_{self.camera_id}_{timestamp}.npy")
        np.save(filename, self.frame_buffer[:self.frames_counter])
        print(f"Saved buffer to {filename}")

class CameraHandler:
    def __init__(self, log_dir='.'):
        self.command_queue_1m = multiprocessing.Queue()
        self.command_queue_640 = multiprocessing.Queue()

        self.process_1m = multiprocessing.Process(target=self.run_camera, args=("PI 1M", log_dir, self.command_queue_1m))
        self.process_640 = multiprocessing.Process(target=self.run_camera, args=("PI 640i", log_dir, self.command_queue_640))

    @staticmethod
    def run_camera(name, log_dir, command_queue):
        camera = Camera(name, log_dir)
        
        while True:
            command = command_queue.get()  #block until a command is received
            print(f"[{name}] Received command: {command}")

            if command == "start":
                print(f"[{name}] Starting acquisition...")
                camera.start_acquiring()
                camera.acquire_frames()
            elif command == "stop":
                print(f"[{name}] Stopping acquisition...")
                camera.stop_acquiring()
            elif command == "exit":
                print(f"[{name}] Exiting process...")
                break  #exit the loop 

    def start_cameras(self):
        self.process_1m.start()
        self.process_640.start()

        time.sleep(1) #processes time to fully initialize
        
        self.command_queue_1m.put("start")
        self.command_queue_640.put("start")

    def stop_cameras(self):
        self.command_queue_1m.put("stop")
        self.command_queue_640.put("stop")
        self.command_queue_1m.put("exit")
        self.command_queue_640.put("exit")

        self.process_1m.join()
        self.process_640.join()

if __name__ == "__main__":
    log_dir = "camera_logs"
    handler = CameraHandler(log_dir)

    try:
        handler.start_cameras()
        time.sleep(10)  # Run for 10 seconds
    except KeyboardInterrupt:
        pass
    finally:
        handler.stop_cameras()  
