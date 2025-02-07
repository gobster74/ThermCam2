import asyncio
from camera import Camera
from cam_handler import CameraHandler

async def acquire_frames_concurrently(camera1: Camera, camera2: Camera):
    #creates two tasks to get frames
    task1 = asyncio.create_task(camera1.acquire_frames())
    task2 = asyncio.create_task(camera2.acquire_frames())
    #wait to finish the tasks
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    camera1 = Camera("PI 1M", "camera_logs")
    camera2 = Camera("PI 640i", "camera_logs")
    camera_handler = CameraHandler(camera1, camera2)

    #start the cameras
    camera_handler.start_cameras()
    camera_handler.start_recording()

    try:
        #frame acquisition for both cameras
        asyncio.run(acquire_frames_concurrently(camera1, camera2))
    except KeyboardInterrupt:
        pass
    finally:
        camera_handler.stop_recording()
