import os
import torch
import numpy as np
from PIL import Image
import cv2
from ultralytics import YOLO
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import get_image_size, get_single_tag_keys
import requests
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

class SAMModel(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super(SAMModel, self).__init__(**kwargs)
        
        self.model = YOLO('yolov8n-seg.pt')
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"YOLO segmentation model loaded on {self.device}")
    
    def predict(self, tasks, **kwargs):
        """Предсказание с помощью YOLO сегментации"""
        predictions = []
        
        for task in tasks:
            # Получаем URL изображения
            image_url = task['data'].get('image')
            if not image_url:
                predictions.append({"result": []})
                continue
            
            # Загружаем изображение
            image = self.load_image(image_url)
            if image is None:
                predictions.append({"result": []})
                continue
            
            try:
                # Выполняем сегментацию
                results = self.model(image)
                
                # Конвертируем результаты в формат Label Studio
                ls_results = []
                for result in results:
                    if result.masks is not None:
                        for i, mask in enumerate(result.masks.data):
                            # Конвертируем маску в полигон
                            polygon_result = self.mask_to_polygon(mask.cpu().numpy(), task['data'])
                            if polygon_result:
                                ls_results.append(polygon_result)
                
                predictions.append({"result": ls_results})
                
            except Exception as e:
                logger.error(f"Error in prediction: {e}")
                predictions.append({"result": []})
        
        return predictions
    
    def load_image(self, image_url):
        """Загрузка изображения по URL"""
        try:
            if image_url.startswith('http'):
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
            else:
                # Локальный файл
                image_path = image_url.replace('/data/upload/', '/label-studio/data/upload/')
                image = Image.open(image_path)
            
            # Конвертируем в numpy array
            image = np.array(image.convert('RGB'))
            return image
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return None
    
    def mask_to_polygon(self, mask, image_data):
        """Конвертация маски в полигон для Label Studio"""
        try:
            # Находим контуры
            mask_uint8 = (mask * 255).astype(np.uint8)
            contours, _ = cv2.findContours(
                mask_uint8, 
                cv2.RETR_EXTERNAL, 
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            if not contours:
                return None
            
            # Берем самый большой контур
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Упрощаем контур
            epsilon = 0.005 * cv2.arcLength(largest_contour, True)
            simplified_contour = cv2.approxPolyDP(largest_contour, epsilon, True)
            
            # Конвертируем в формат Label Studio
            height, width = mask.shape[:2]
            points = []
            
            for point in simplified_contour:
                x = float(point[0][0]) / width * 100
                y = float(point[0][1]) / height * 100
                points.extend([x, y])
            
            return {
                "value": {
                    "points": points,
                    "closed": True
                },
                "type": "polygonlabels",
                "from_name": "label",
                "to_name": "image"
            }
        except Exception as e:
            logger.error(f"Error converting mask to polygon: {e}")
            return None
