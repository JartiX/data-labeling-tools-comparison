from PIL import Image # pip install Pillow
import os

gif_path = 'src/gif/subaru-rally-wrc-subaru.gif'
output_folder = 'src/gif/frames'

os.makedirs(output_folder, exist_ok=True)

with Image.open(gif_path) as im:
    for i in range(im.n_frames):
        im.seek(i)
        im.save(f'{output_folder}/frame_{i:03}.png')