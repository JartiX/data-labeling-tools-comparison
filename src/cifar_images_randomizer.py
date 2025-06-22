import os
import random
import shutil
import string
from pathlib import Path
import kagglehub # pip install kagglehub

def get_random_filename(extension="png", length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) + '.' + extension

def download_dataset_if_needed(dataset_dir):
    dataset_path = Path(dataset_dir)
    if not dataset_path.exists():
        path = kagglehub.dataset_download("ayush1220/cifar10")
        print("Датасет установлен по пути:", path)
        return path
    else:
        print("Датасет уже существует по пути:", dataset_path)
        return dataset_path

def collect_random_images(source_dir, target_dir, num_images_per_class=10):
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    for class_folder in sorted(source_path.iterdir()):
        if class_folder.is_dir():
            images = list(class_folder.glob("*.*"))
            selected_images = random.sample(images, min(num_images_per_class, len(images)))

            for image in selected_images:
                new_name = get_random_filename(extension=image.suffix.lstrip('.'))
                shutil.copy(image, target_path / new_name)
                print(f"Копирован {image} -> {target_path / new_name}")

if __name__ == "__main__":
    home_dir = os.getenv('HOME') or os.getenv('USERPROFILE')
    dataset_root = download_dataset_if_needed(f"{os.path.join(home_dir, '.cache', 'kagglehub', 'datasets', 'ayush1220', 'cifar10', 'versions', '2', 'cifar10')}")
    train_dataset_root = os.path.join(dataset_root, "train")
    collect_random_images(train_dataset_root, "datasets/CIFAR-10-randomized", num_images_per_class=10)
