# Label studio

## Установка:

1. Перейти в директорию runners/Label Studio

```
cd "runners/Label Studio"
```

2. Создать директорию data, если её нет

```
mkdir data
```

При использовании Linux/macOS выполнить следующую команду:
```
sudo chown -R 1001:1001 data
```

3. Убедиться что порт 8081 свободен и запустить Label Studio

```
docker-compose up -d
```

## Веб интерфейс доступен по ссылке localhost:8081

## Остановка:

```
docker compose down
```

## Проверка логов:

```
docker-compose logs -f
```

## Развёртка сервиса на платформе виртуализации proxmox

1. Создаем директорию label_studio  
```
mkdir label_studio
cd label_studio
```
```

2. Создаем директорию data и даём доступ пользователю 1001  
```
mkdir data
sudo chown -R 1001:1001 data
```

3. Создаем docker-compose.yml
```
nano docker-compose.yml

4. Вводим в docker-compose.yml следующий код, проверьте доступность порта 8081, при необходимости сменить
```
version: '3.8'

services:
  label-studio:
    image: heartexlabs/label-studio:latest
    container_name: label-studio
    ports:
      - "8081:8080"
    volumes:
      - ./data:/label-studio/data
    restart: unless-stopped
    user: "1001:1001"
    environment:
      - LABEL_STUDIO_ML_BACKEND_V2=true
```

## Важно!

* Для работы **необходимо**, чтобы на системе был установлен [docker и docker compose](../docker_install.md).