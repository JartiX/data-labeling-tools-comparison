# Data Labeling Tools Comparison

Комплексное сравнение популярных инструментов разметки данных для машинного обучения: **CVAT** и **Label Studio**.

## Цель проекта

Провести детальный анализ и сравнение современных инструментов разметки данных для выбора оптимального решения под различные задачи машинного обучения в ИСЗФ СО РАН.

## Сравниваемые инструменты

| Инструмент | Специализация | Лицензия | Поддерживаемые данные |
|------------|---------------|----------|----------------------|
| **[CVAT](https://www.cvat.ai/)** | Компьютерное зрение | MIT | Изображения, видео, 3D |
| **[Label Studio](https://labelstud.io/)** | Универсальная разметка | Apache 2.0 | Изображения, текст, аудио, видео, временные ряды |

## Структура проекта

```
data-labeling-tools-comparison/
├── runners/                          # Скрипты развертывания
│   ├── CVAT_runner/
│   │   ├── Makefile                  # Автоматизация развертывания CVAT
│   │   └── cvat/                     # Клонированный репозиторий CVAT
│   └── Label Studio/
|       └── data/                     # Директория с данными Label Studio
│       └── docker-compose.yml        # Конфигурация Label Studio
├── docs/                             # Документация
│   ├── CVAT/                         # Документация по CVAT
│   ├── Label Studio/                 # Документация по Label Studio
|   └── evaluation/                   # Сравнение инструментов
│   └── problems/                     # Решенные проблемы
├── src/                              # Исходный код
│   ├── tests/                        # Нагрузочные тесты
│   └── gif/                          # Конвертеры для работы с GIF
|   └── ms_coco/                      # Сборка кастомного датасета MS COCO
|   └── cifar_images_randomizer.py    # Случайная сборка датасета CIFAR-10
|   └── fit_to_png.py                 # Конвертер fit в png
|   └── remove_broken_images.py       # Автоудаление поврежденных изображений
|   └── time_data_preprocess.py       # Подготовка временного датасета
└── imgs/                             # Скриншоты и изображения
```

## Быстрый старт

### Требования

- [Docker и Docker Compose](docs/docker_install.md)
- Make (для CVAT)
- Python 3.8+ (для тестов)
- 8GB+ RAM
- 20GB+ свободного места

### Развертывание CVAT

```bash
cd runners/CVAT_runner
make up                    # Полное развертывание
make createsuperuser      # Создание администратора
```

Доступ: http://localhost:8080

### Развертывание Label Studio

```bash
cd "runners/Label Studio"
mkdir data && sudo chown -R 1001:1001 data  # Linux/macOS
docker-compose up -d
```

Доступ: http://localhost:8081

## Результаты [сравнения](./docs/evaluation/final_mark.md)

### Основные выводы

| Критерий | Label Studio | CVAT | Победитель |
|----------|--------------|------|------------|
| **Универсальность** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Label Studio |
| **Компьютерное зрение** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | CVAT |
| **Простота использования** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Label Studio |
| **Производительность** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | CVAT |
| **Стоимость** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | CVAT |

### Детальное сравнение

#### Работа с видео
- **CVAT**: Продвинутый трекинг, интерполяция, автоматическое отслеживание
- **Label Studio**: Базовая поддержка видео, простая интерполяция

#### Текст и NLP
- **CVAT**: Не поддерживается
- **Label Studio**: NER, классификация, sentiment analysis

#### Скорость разметки
- **Классификация**: Label Studio 728 изображений/час vs CVAT 514 изображений/час
- **Детекция**: CVAT 167 изображений/час vs Label Studio 116 изображений/час

#### Лицензирование
- **CVAT**: Полностью open-source (MIT)
- **Label Studio**: Community (Apache 2.0) + Enterprise ($99/месяц)

## Рекомендации по использованию

### Выбирайте CVAT, если:
- Основная задача — компьютерное зрение
- Работаете с видео и нужен трекинг объектов
- Требуется максимальная производительность детекции
- Ограниченный бюджет (полностью бесплатный)
- Нужна LDAP интеграция без доплат

### Выбирайте Label Studio, если:
- Работаете с разными типами данных (текст, аудио, изображения)
- Нужна быстрая классификация изображений
- Требуется кастомизация интерфейса
- Планируется работа с временными рядами
- Нужна простота освоения для новых пользователей

## Проведенные тесты

### Функциональные тесты
- Разметка изображений (bounding boxes, полигоны)
- Работа с видео (трекинг, интерполяция)
- Классификация текста и NER
- Анализ временных рядов
- Разметка табличных данных

### Нагрузочные тесты
- 5 одновременных пользователей
- Измерение потребления CPU/RAM

### Скоростные тесты
- Классификация CIFAR-10 (100 изображений)
- Детекция MS COCO (50 изображений, 3-4 объекта)

## Документация

### Руководства по установке
- [Установка CVAT](docs/cvat/readme.md)
- [Установка Label Studio](docs/Label%20Studio/README.md)
- [Настройка ML-моделей для CVAT](docs/CVAT/ml_models_install.md)
- [Настройка ML-моделей для Label Studio](docs/Label%20Studio/ml_backend_integration.md)

### Решение проблем
- [Проблемы CVAT и их решения](docs/problems/cvat_problems.md)
- [Проблемы Label Studio](docs/problems/label_studio_problems.md)
- [Настройка облачного хранилища](docs/CVAT/contain_data_in_cloud.md)

### Сравнительный анализ
- [Итоговая сравнительная таблица](docs/evaluation/final_mark.md)
- [Скоростные тесты](docs/evaluation/speed_test.md)
- [Тестирование специальных типов данных](docs/evaluation/special_labeling_models.md)
- [UX и коллаборация](docs/evaluation/ux_and_collaboration.md)
- [Нагрузочные тесты и лицензии](docs/evaluation/weight_and_license.md)
- [Интеграция ML](docs/evaluation/ML_integration.md)
- [Разметка GIF](docs/evaluation/gif_annotation.md)
- [Разметка видео](docs/evaluation/video_annotation.md)

## Техническая информация

### Архитектура CVAT
- **Backend**: Django + PostgreSQL + Redis
- **Frontend**: React
- **Контейнеризация**: Docker Compose (multi-service)
- **ML интеграция**: Nuclio serverless functions

### Архитектура Label Studio
- **Backend**: Django + SQLite/PostgreSQL
- **Frontend**: React
- **Контейнеризация**: Docker (single container)
- **ML интеграция**: ML Backend + REST API

### Системные требования

| Компонент | CVAT | Label Studio |
|-----------|------|--------------|
| **RAM** | 6-16 GB | 4-8 GB |
| **CPU** | 4+ cores | 2+ cores |
| **Disk Free Space** | 10+ GB | 5+ GB |
| **GPU** | Опционально (ML) | Опционально (ML) |

## Запуск тестов

### Нагрузочное тестирование

```bash
# Установка зависимостей
pip install locust

# Тест CVAT
cd src/tests
locust -f cvat_test.py --host=http://localhost:8080 --users=5 --spawn-rate=1

# Тест Label Studio
# Создать tokens.py для тестовых пользователей
locust -f label_studio_test.py --host=http://localhost:8081 --users=5 --spawn-rate=1
```

### Создание тестовых датасетов

```bash
# CIFAR-10 для классификации
python src/cifar_images_randomizer.py

# MS COCO для детекции
python src/ms_coco/dataset_parser.py
```


## Проект создан в рамках технологической практики студента направления "Прикладная информатика" ИГУ.

### Авторы
- **Студент**: А.М. Пилявин
- **Руководитель**: А.М. Веснин (ст. преподаватель)
- **Организация**: ИСЗФ СО РАН

## Лицензия

Проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для деталей.

## Полезные ссылки

### Официальная документация
- [CVAT Documentation](https://opencv.github.io/cvat/docs/)
- [Label Studio Documentation](https://labelstud.io/guide/)

### Связанные проекты
- [CVAT GitHub](https://github.com/opencv/cvat)
- [Label Studio GitHub](https://github.com/heartexlabs/label-studio)
- [Label Studio ML Backend](https://github.com/HumanSignal/label-studio-ml-backend)

### Дополнительные ресурсы
- [Docker Documentation](https://docs.docker.com/)
- [Nuclio Serverless Platform](https://nuclio.io/)
- [Google Cloud Storage](https://cloud.google.com/storage)
