import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image, ImageSequence
import os
import numpy as np

def tif_to_gif(tif_path, gif_path):
    """Convert a multi-frame TIF image to a GIF."""
    with Image.open(tif_path) as img:
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], loop=0, duration=200)

def display_gifs_with_matplotlib(gif_paths):
    fig, axes = plt.subplots(1, len(gif_paths), figsize=(15, 5))
    anims = []
    
    legends = ['Train Volume', 'Train Labels', 'Test Volume']  # Add your legends here

    for ax, gif_path, legend in zip(axes, gif_paths, legends):
        ax.axis('off')
        with Image.open(gif_path) as img:
            frames = [np.array(frame.copy()) for frame in ImageSequence.Iterator(img)]

        ims = [[ax.imshow(frame, animated=True, cmap='gray')] for frame in frames]
        ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True)
        anims.append(ani)
        
        ax.set_title(legend)  # Add title as legend

    plt.show()

if __name__ == "__main__":
    # File directory
    dir_data = 'sample_isbi/'  # Update this path to your actual file location

    # TIF files to read
    tif_files = ['train-volume.tif', 'train-labels.tif', 'test-volume.tif']

    # Convert each TIF file to GIF and store its path
    gif_paths = []
    for tif_file in tif_files:
        tif_path = os.path.join(dir_data, tif_file)
        gif_path = os.path.join(dir_data, f"{os.path.splitext(tif_file)[0]}.gif")
        tif_to_gif(tif_path, gif_path)
        gif_paths.append(gif_path)

    # Display the generated GIFs using Matplotlib
    display_gifs_with_matplotlib(gif_paths)