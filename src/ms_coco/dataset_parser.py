import json
import random
import numpy as np
from pycocotools.coco import COCO # pip install pycocotools
import os
import requests
from tqdm import tqdm

save_dir = 'datasets/ms_coco_dataset'
os.makedirs(save_dir, exist_ok=True)

annotation_file = 'src/ms_coco/annotations/instances_train2017.json'
annotation_url = 'https://huggingface.co/datasets/merve/coco/resolve/main/annotations/instances_train2017.json?download=true'
os.makedirs(os.path.dirname(annotation_file), exist_ok=True)

if not os.path.exists(annotation_file):
    print("Аннотационный файл не найден. Скачиваем...")
    try:
        response = requests.get(annotation_url, stream=True)
        response.raise_for_status()
        with open(annotation_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Аннотация успешно скачана.")
    except Exception as e:
        print(f"Ошибка при скачивании аннотации: {e}")
        exit(1)
        
coco = COCO(annotation_file)

# ID интересующих категорий
cat_ids = coco.getCatIds(catNms=['person', 'bicycle', 'car'])

# Получение всех изображений, содержащих хотя бы одну из этих категорий
img_ids = coco.getImgIds(catIds=cat_ids)

filtered_images = []

for img_id in img_ids:
    anns = coco.loadAnns(coco.getAnnIds(imgIds=img_id, catIds=cat_ids))

    anns = [ann for ann in anns if ann['category_id'] in cat_ids]
    if len(anns) >= 3 and len(anns) <= 4:
        filtered_images.append({
            'image_id': img_id,
            'annotations': anns
        })
    if len(filtered_images) >= 50:
        break

with open(os.path.join(save_dir, 'filtered_images.json'), 'w') as f:
    json.dump(filtered_images, f)

print(f"Отфильтровано {len(filtered_images)} изображений.")


# Скачивание изображений
for img_info in tqdm(filtered_images):
    img_id = img_info['image_id']
    img_data = coco.loadImgs(img_id)[0]
    img_url = f'http://images.cocodataset.org/train2017/{img_data["file_name"]}'
    img_path = os.path.join(save_dir, img_data['file_name'])
    if not os.path.exists(img_path):
        try:
            img = requests.get(img_url, stream=True)
            with open(img_path, 'wb') as f:
                for chunk in img.iter_content(1024):
                    f.write(chunk)
        except Exception as e:
            print(f"Ошибка при скачивании {img_url}: {e}")
