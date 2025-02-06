import ctypes
import os
import time
import pyOptris as optris
import numpy as np
import cv2

camera_id = {
    'PI 1M': '17092037.xml', 
    'PI 640i': '6060300.xml',
}
log_dir = '.'

class Camera: 
    def __init__(self, type, log_dir = '.'):
        self.type = type
        self.log_dir = log_dir
        self.is_recording = True
        self.max_buffer_size = 1000 
        self.camera_id = None

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
                
        self.log_file = os.path.join(
            self.log_dir, f"log_{self.type}_{int(time.time())}.log"
        )
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

        err, self.camera_id = optris.multi_usb_init(
            config_file, None, self.log_file
        )

        if err != 0:
            print(f"Failed to initialize {self.type}: error Code {err}")
            self.camera_id = None
        else:
            self.camera_id = self.camera_id.value 
            serial = optris.get_multi_get_serial(self.camera_id)
            print(f"{self.type} camera initialized successfully. camera serial: {serial}")
            self.w, self.h, err = optris.get_multi_thermal_image_size(self.camera_id)

    def start_acquiring(self):
        if not self.camera_id:
            print(f"Error starting the camera")
            return 
        self.is_recording = True
        print(f"Starting recording")

    def acquire_frames(self):  
        if not self.camera_id:
            print("Camera did not start, no frames are being saved.")
            return
        print(f"Starting frame acquisition...")
        frames_counter = 0
        self.frame_buffer = np.empty((self.max_buffer_size, self.h, self.w), dtype=np.uint16)

        try:
            start_time = time.time()
            while self.is_recording:
                frame, err = optris.get_multi_thermal_image(self.camera_id, self.w, self.h)
                if int(err) == 0:
                    # Process the frame for display
                    frame_data = np.frombuffer(frame, dtype=np.uint16).reshape(self.h, self.w)

                    # Normalize the frame for display (0-255)
                    frame_display = self.process_frame_for_display(frame_data)

                    # Show the frame in real-time
                    cv2.imshow('Thermal Frame', frame_display)

                    # Save the frame into the buffer
                    self.frame_buffer[frames_counter] = frame_data
                    frames_counter += 1

                    print(f"Acquired frame {frames_counter}/{self.max_buffer_size}")

                    if frames_counter == self.max_buffer_size:
                        print(f"Buffer full: {frames_counter} frames.")
                        self.stop_acquiring()
                        self.change_roi(x=np.random.randint(0, 400), y=np.random.randint(0, 300))
                else:
                    print(f"Error {int(err)} occurred while acquiring frame.")

                # To make sure the window is responsive and that the frame acquisition continues smoothly
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to stop
                    break

        except Exception as e:
            print(f"Error: {e}")

        print(f"Stopping recording, last frame acquired: {frames_counter}")
        cv2.destroyAllWindows()

    def process_frame_for_display(self, frame):
        # Normalize the frame to 0-255 for 8-bit display
        frame_normalized = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
        frame_normalized = frame_normalized.astype(np.uint8)
        return frame_normalized

    def stop_acquiring(self, save_dir='frames'):
        if not self.camera_id:
            print("Camera not initialized, cannot stop acquiring.")
            return

        self.is_recording = False
        self.save_buffer(save_dir)
        print("Recording stopped and frames saved")

    def save_buffer(self, save_dir="frames"):
        os.makedirs(save_dir, exist_ok=True)
        timestamp = int(time.time())
        filename = os.path.join(save_dir, f"frames_{self.camera_id}_{timestamp}.npy")
        np.save(filename, np.array(self.frame_buffer, dtype=np.float32))
        print(f"Saved buffer to {filename}")

    def change_roi(self, x=None, y=None):
        self.position = optris.set_multi_clipped_format_position(self.camera_id, x, y)


if __name__ == "__main__":
    log_dir = "camera_logs"
    save_dir = "frames"

    camera = Camera("PI 640i", log_dir)
    camera.start_acquiring()

    try: 
        camera.acquire_frames()
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop_acquiring()
