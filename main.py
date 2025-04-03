import asyncio
import openUa
import multiprocessing
import obj

log_dir = "camera_logs"

def run_open_ua(command_queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        camera_handler = obj.CameraHandler(log_dir) 
        loop.run_until_complete(openUa.run_open_ua(camera_handler, command_queue))
    finally:
        loop.close()

async def main():
    command_queue = multiprocessing.Queue()
    process_open_ua = multiprocessing.Process(target=run_open_ua, args=(command_queue,))

    camera_handler = obj.CameraHandler(log_dir)
    #camera_handler.start_cameras()

    process_open_ua.start()

    try:
        while True: 
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        print("Stopping processes...")

    camera_handler.stop_cameras()
    process_open_ua.terminate()
    process_open_ua.join()

if __name__ == "__main__":
    asyncio.run(main())
