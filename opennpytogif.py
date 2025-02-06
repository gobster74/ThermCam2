import numpy as np
import imageio.v3 as imageio
import os
import matplotlib.pyplot as plt

def read_npy_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    data = np.load(filename)
    print(f"Loaded data shape: {data.shape}")
    return data

def create_frames(data, width=None, height=None):
    if data.ndim == 4 and data.shape[-1] == 3:  
        print("Detected color data.")
        frames = [
            ((frame - frame.min()) / (frame.max() - frame.min()) * 255).astype(np.uint8)
            for frame in data
        ]
    elif data.ndim == 3:  
        print("Detected grayscale data.")
        frames = [
            ((frame - frame.min()) / (frame.max() - frame.min()) * 255).astype(np.uint8)
            for frame in data
        ]
    elif data.ndim == 1 and width and height:  
        print("Reshaping flat grayscale data into frames...")
        num_frames = len(data) // (width * height)
        frames = []
        for i in range(num_frames):
            frame = data[i * width * height : (i + 1) * width * height].reshape((height, width))
            normalized_frame = (frame - frame.min()) / (frame.max() - frame.min()) * 255
            frames.append(normalized_frame.astype(np.uint8))
    else:
        raise ValueError("Unexpected data shape.")
    print(f"Generated {len(frames)} frames.")
    return frames

def apply_colormap(frames):
    print("Applying colormap to grayscale frames...")
    color_frames = [plt.cm.viridis(frame / 255.0)[:, :, :3] * 255 for frame in frames]
    return [frame.astype(np.uint8) for frame in color_frames]

def save_as_gif(frames, output_file, fps):
    if not frames:
        raise ValueError("No frames to save.")
    print(f"Saving GIF with {len(frames)} frames at {fps} FPS...")
    imageio.imwrite(output_file, frames, format='GIF', fps=fps)
    print(f"GIF saved to {output_file}")

if __name__ == "__main__":
    npy_file = r'frames\frames_1_1734004625.npy'
    output_gif = 'frame_to_gif1.gif'
    frame_width = 640
    frame_height = 480
    frames_per_second = 10

    try:
        data = read_npy_file(npy_file)
        frames = create_frames(data, width=frame_width, height=frame_height)
        if data.ndim == 3: 
            frames = apply_colormap(frames)
        save_as_gif(frames, output_gif, frames_per_second)
    except Exception as e:
        print(f"Error: {e}")
