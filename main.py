import asyncio
import openUa
import threading
import obj
log_dir = "camera_logs"

def run_open_ua(camera):
    # Create a new event loop
    loop = asyncio.new_event_loop()
    # Set the event loop for the current context
    asyncio.set_event_loop(loop)
    try:
        # Run OpenUa in this thread and call the camera's method
        loop.run_until_complete(openUa.run_open_ua(camera))
    finally:
        # Close the event loop
        loop.close()
def run_camera(camera):
    while True: camera.aquire_frames()
async def main():
    camera = obj.Camera("PI 1M", log_dir)
    # Create threads for OpenUa and Camera
    thread1 = threading.Thread(target=run_open_ua, args=(camera,))
    thread2 = threading.Thread(target=run_camera, args=(camera,))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()    
    thread2.join()


if __name__ == "__main__":
    asyncio.run(main())

    