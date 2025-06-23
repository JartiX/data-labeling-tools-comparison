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

4. Смотрим какие порты используют наши модели.  
Это важный пункт, посколько в function.yaml порт не указан и велика вероятность получить следующую ошибку:
![](../../imgs/port%20error.png)  
Посмотреть порты можно так: `docker ps | egrep 'dextr|yolo'`  
Примерный вывод, нас тут интересует внешний порт (в данном случае 53027 и 53025):
```
99b46b9fbcdd   cvat.openvino.dextr:latest                   "processor"              11 minutes ago   Up 11 minutes (healthy)   0.0.0.0:53027->8080/tcp                                  nuclio-nuclio-dextr_task
ca190ba7b25e   cvat.openvino.omz.public.yolo-v3-tf:latest   "processor"              2 days ago       Up 13 hours (healthy)     0.0.0.0:53025->8080/tcp                                  nuclio-nuclio-yolo-v3
```

5. Добавляем указание портов в function.yaml для каждой из моделей  

Необходимо добавить поле httpPort в spec с портом из docker
```
spec:
  description: Deep Extreme Cut
  runtime: 'python:3.8'
  handler: main:handler
  eventTimeout: 30s
  httpPort: 53027
```  
Проделываем это для каждого function.yaml  
```
nano serverless/openvino/dextr/nuclio/function.yaml
nano serverless/openvino/omz/public/yolo-v3-tf/nuclio/function.yaml
```

6. Создаем функции в nuclio  
``` 
nuctl deploy dextr_task --platform local --project-name cvat --path serverless/openvino/dextr/nuclio --runtime python --handler main:handler
nuctl deploy yolo-v3 --platform local --project-name cvat --path serverless/openvino/omz/public/yolo-v3-tf/nuclio --runtime python --handler main:handler
```

### Для Linux:

```
./serverless/deploy_cpu.sh serverless/openvino/dextr
./serverless/deploy_cpu.sh serverless/openvino/omz/public/yolo-v3-tf
```

## После этого можно зайти на [Nuclio Web](http://localhost:8070) и проверить, что там появились добавленные функции

## Далее, модели можно использовать в качестве детектора (yolo) и интерактора (dextr)

![](../../imgs/models%20in%20cvat.png)