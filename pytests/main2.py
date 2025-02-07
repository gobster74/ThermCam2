import asyncio
import threading
import time
from camera_handler import CameraHandler
import openUa

def run_open_ua(camera_handler):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(openUa.run_open_ua(camera_handler))
    finally:
        loop.close()
def run_cameras(camera_handler):
    camera_handler.start_recording()
    for i in range(3):
        camera_handler.send_data_block_index(i)
        time.sleep(0.5) 

    camera_handler.stop_recording()

async def main():
    camera_handler = CameraHandler(log_dir="camera_logs", config_csv="data_blocks.csv")
    thread1 = threading.Thread(target=run_open_ua, args=(camera_handler,))
    thread2 = threading.Thread(target=run_cameras, args=(camera_handler,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    asyncio.run(main())

