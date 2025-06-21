# Установка моделей машинного обучения в CVAT

> На Windows все команды должны быть введены в [WSL](../wsl_download.md)

> Все последующие команды вводятся из директории runners/CVAT_runner/cvat (```cd runners/CVAT_runner/cvat```)

## 1. Устанавливаем Nuclio по [этой документации](../nuclio_download.md)

## 2. Устанавливаем модели (для примера взяты подготовленные из репозитория cvat)

### Для Windows:

1. Устанавливаем Docker в WSL по [этой документации](../docker_to_wsl.md)

2. Создаем проект cvat  
``` nuctl create project cvat --platform local```

3. Собираем образ dextr и yolo-v3  
``` 
docker build -t cvat.openvino.dextr.base serverless/openvino/dextr/nuclio
docker build -t cvat.openvino.omz.public.yolo-v3-tf.base serverless/openvino/omz/public/yolo-v3-tf/nuclio
```

4. Создаем функции в nuclio  
``` 
nuctl deploy dextr_task --platform local --project-name cvat --path serverless/openvino/dextr/nuclio --runtime python --handler main:handler
nuctl deploy yolo-v3 --platform local --project-name cvat --path serverless/openvino/omz/public/yolo-v3-tf/nuclio --runtime python --handler main:handler
```

### Для Linux:

```
./serverless/deploy_cpu.sh serverless/openvino/dextr
./serverless/deploy_cpu.sh serverless/openvino/omz/public/yolo-v3-tf
```

## После этого можно зайти на [Nuclio Web](localhost:8070) и проверить, что там появились добавленные функции

## Далее, модели можно использовать в качестве детектора (yolo) и интерактора (dextr)

![](../../imgs/models%20in%20cvat.png)