import os
import numpy as np
from astropy.io import fits
from PIL import Image
import argparse


def convert_fit_to_png(fit_path, png_path=None, vmin=None, vmax=None):
    try:
        with fits.open(fit_path) as hdul:
            data = hdul[0].data

        if data is None or data.ndim != 2:
            print(f"Пропущено (не 2D): {fit_path}")
            return

        # Нормализация
        if vmin is None:
            vmin = np.nanmin(data)
        if vmax is None:
            vmax = np.nanmax(data)

        norm_data = (data - vmin) / (vmax - vmin)
        norm_data = np.clip(norm_data, 0, 1)
        img_data = (norm_data * 255).astype(np.uint8)

        # Сохраняем PNG
        image = Image.fromarray(img_data)
        if png_path is None:
            png_path = os.path.splitext(fit_path)[0] + ".png"
        image.save(png_path)
    except Exception as e:
        print(f"Ошибка при конвертации {fit_path}: {e}")

def batch_convert_fits_in_directory(directory_path, png_dir=None, vmin=None, vmax=None):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".fit") or filename.lower().endswith(".fits"):
            fit_path = os.path.join(directory_path, filename)
            if os.path.isfile(fit_path):
                convert_fit_to_png(fit_path, png_path=os.path.join(png_dir, os.path.splitext(filename)[0] + ".png") if png_dir else None, vmin=vmin, vmax=vmax)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Конвертация FIT файлов в формат PNG.")
    parser.add_argument("--directory", type=str, help="Папка с FIT файлами.")
    parser.add_argument("--png_dir", type=str, help="Директория для сохранения PNG файла (если не указан, сохраняется рядом с FIT файлом).")
    parser.add_argument("--vmin", type=float, help="Минимальное значение для нормализации.")
    parser.add_argument("--vmax", type=float, help="Максимальное значение для нормализации.")
    args = parser.parse_args()
    if args.png_dir and not os.path.exists(args.png_dir):
        os.makedirs(args.png_dir)
    batch_convert_fits_in_directory(args.directory, png_dir=args.png_dir, vmin=args.vmin, vmax=args.vmax)
