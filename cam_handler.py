from camera import Camera

class CameraHandler:
    def __init__(self, camera1: Camera, camera2: Camera):
        self.camera1 = camera1
        self.camera2 = camera2
    
    def start_cameras(self):
        print("Starting both cameras...")
        self.camera1.start_acquiring()
        self.camera2.start_acquiring()

    def stop_cameras(self):
        print("Stopping both cameras...")
        self.camera1.stop_acquiring()
        self.camera2.stop_acquiring()
    
    def start_recording(self):
        print("Starting recording for both cameras...")
        self.camera1.start_acquiring()
        self.camera2.start_acquiring()

    def stop_recording(self):
        print("Stopping recording for both cameras...")
        self.camera1.stop_acquiring()
        self.camera2.stop_acquiring()

    def send_data_block(self, block_id: int):
        print(f"Sending data block {block_id} to both cameras...")
        self.camera1.set_data_block(block_id)
        self.camera2.set_data_block(block_id)
