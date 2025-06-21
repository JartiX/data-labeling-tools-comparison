# Поддержка форматов датасетов: CVAT vs Label Studio

## CVAT (Computer Vision Annotation Tool)

### Поддерживаемые форматы импорта:
- **COCO** - Полная поддержка
  - Импорт аннотаций для detection, segmentation, keypoints
  - Поддержка категорий и атрибутов
  - Сохранение метаданных изображений

- **YOLO** - Полная поддержка
  - YOLOv5/YOLOv8 format
  - Автоматическое определение классов
  - Поддержка нормализованных координат

- **Pascal VOC** - Полная поддержка
  - XML формат аннотаций
  - Поддержка bounding boxes
  - Импорт информации о сложности объектов

### Поддерживаемые форматы экспорта:
- COCO JSON
- YOLO txt
- Pascal VOC XML
- CVAT XML (нативный формат)
- TensorFlow Records
- MOT (Multiple Object Tracking)
- LabelMe JSON  
и множество других форматов

## 1.2 Label Studio

### Поддерживаемые форматы импорта:
- COCO, YOLO, PASCAL VOC XML - только через конвертер

### Поддерживаемые форматы экспорта:
- COCO JSON
- Pascal VOC XML
- YOLO
- Label Studio JSON (нативный)
- CSV
- TSV
- Brush labels (для сегментации)

## Результаты  
| Критерий | CVAT | Label Studio | Победитель |
|----------|------|--------------|------------|
| COCO поддержка | ⭐⭐⭐⭐⭐ | ⭐⭐ | CVAT |
| YOLO поддержка | ⭐⭐⭐⭐⭐ | ⭐⭐ | CVAT |
| Pascal VOC поддержка | ⭐⭐⭐⭐⭐ | ⭐⭐ | CVAT |
