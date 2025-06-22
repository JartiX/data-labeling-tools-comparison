
# При попытке разметить анимацию (gif) в обоих инструментах, сразу сталкиваемся с проблемой, что разметить gif напрямую нельзя. При попытке его загрузить и разметить label studio проигрывает всё gif и можно поставить один единственный bbox, а cvat в свою очередь предлагает разметить только первый кадр.  
## Варианты решения:  
### 1. Разбить gif на отдельные png/jpg кадры и загрузить их как отдельные задачи. [Исходный код](../../src/gif/gif_to_frames.py)
```
from PIL import Image # pip install Pillow
import os

gif_path = 'your_file.gif'
output_folder = 'frames'

os.makedirs(output_folder, exist_ok=True)

with Image.open(gif_path) as im:
    for i in range(im.n_frames):
        im.seek(i)
        im.save(f'{output_folder}/frame_{i:03}.png')
```  
### 2. Преобразовать gif в mp4 и размечать его как video. [Исходный код](../../src/gif/gif_to_mp4.py) Понадобится ffmpeg ([Как скачать](../ffmpeg_download_guide.md)) 
```
import subprocess

def convert_gif_to_mp4_ffmpeg_only(input_gif_path, output_mp4_path, fps=10):
    """
    Конвертирует GIF в MP4 через ffmpeg.
    :param input_gif_path: Путь к .gif
    :param output_mp4_path: Путь к .mp4
    :param fps: Частота кадров
    """
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',  # перезаписать без подтверждения
        '-i', input_gif_path,
        '-vf', f"fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2",  # чётные размеры
        '-vcodec', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-movflags', 'faststart',
        output_mp4_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"[+] Готовый MP4: {output_mp4_path}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Ошибка ffmpeg: {e}")

input_gif = "path/to/input.gif"
output_mp4 = "path/to/output.mp4"
convert_gif_to_mp4_ffmpeg_only(input_gif, output_mp4)

```