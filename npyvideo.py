import numpy as np
import cv2
import os

def process_thermal_video_with_palette(npy_file, output_video="thermal_output_color.avi"):
    frames = np.load(npy_file)

    height, width = frames.shape[1], frames.shape[2]
    fps = 10  # fps for the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height), isColor=True)

    print(f"Processing {frames.shape[0]} frames from {npy_file}...")

    for i, frame in enumerate(frames):
        normalized_frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
        normalized_frame = normalized_frame.astype(np.uint8)
        colorized_frame = cv2.applyColorMap(normalized_frame, cv2.COLORMAP_JET)

        cv2.imshow('Thermal Frame (Colorized)', colorized_frame)
        out.write(colorized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()
    print(f"Video saved to {output_video}")

if __name__ == "__main__":
    npy_file_path = "./frames/frames_1_1734008165.npy"

    if not os.path.exists(npy_file_path):
        print(f"File not found: {npy_file_path}")
    else:
        process_thermal_video_with_palette(npy_file_path)
