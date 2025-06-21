# Установка моделей машинного обучения в Label Studio


> Все последующие команды вводятся из директории runners/Label Studio (```cd runners/Label Studio```)

## 1. Клонировать репозиторий ML Backend и выбрать нужную модель из готовых
```
git clone https://github.com/HumanSignal/label-studio-ml-backend.git
cd label-studio-ml-backend/label_studio_ml/examples/{необходимая модель}
```

## 2. Отредактировать `docker-compose.yml` файл, находящийся в папке выбранной модели.  
Найти в нём следующие строки и сменить порт на тот, который использует Label Studio и вписать API ключ, сгенерировать который можно в веб-интерфейсе Label Studio в Account & Settings
![](../../imgs/api%20token.png)
```
- LABEL_STUDIO_URL=http://host.docker.internal:8080
- LABEL_STUDIO_API_KEY=
```

## 3. Поднять контейнер ```docker compose up --build -d```

## 4. Перейти в проект и нажать на кнопку settings
![](../../imgs/settings%20btn%20in%20project.png)

## 5. Во вкладке Model нажать Connect Model

## 6. Заполнить поля имени и Backend URL и нажать Validate and Save
> Поскольку мы используем докер для развертки, нужно писать url такого вида: `http://host.docker.internal:{backend-port}`

## В результате подключим нужную нам модель и сможем её использовать для разметки данных
![](../../imgs/yolo%20model.png)