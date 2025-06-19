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