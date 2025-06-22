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

input_gif = "src/gif/subaru-rally-wrc-subaru.gif"
output_mp4 = "src/gif/subaru-rally-wrc-subaru.mp4"
convert_gif_to_mp4_ffmpeg_only(input_gif, output_mp4)
