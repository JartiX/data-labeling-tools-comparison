# Настройка хранения данных CVAT локально

> Для Windows потребуется [WSL](../wsl_download.md) и настройка [docker под wsl](../docker_to_wsl.md)

## 1. Переходим в репозиторий cvat
```
cd runners/CVAT_runner/cvat
```  
> Останавливаем контейнер, если запущен `docker compose down`  

## 2. Создаем папку data, где будут храниться данные
```
mkdir data
```

## 3. Переносим существующие данные, если они были

### 3.1 Ищем название образа данных   
`docker volume ls | grep cvat_data`

### 3.2 Переносим данные в нашу локальную папку

```
docker run --rm -v {название образа данных}:/source -v "$(pwd)/data":/dest alpine cp -r /source/. /dest/
```

## 4. Изменяем docker-compose.override.yml  
Меняем cvat_data volume на такое
```
volumes:
  cvat_data:
    driver: local
    driver_opts:
      type: none
      device: ./data/
      o: bind
```
