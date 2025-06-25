# CVAT

| Команда              | Описание                                                                              |
| ----------------- | ------------------------------------------------------------------------------------- |
| `clone`           | Клонирует репозиторий CVAT, если он ещё не скачан                                     |
| `build`           | Собирает образы контейнеров, предварительно выполнив `clone`                          |
| `up`              | Запускает сервисы CVAT и зависимостей в фоне (`docker compose up -d`) после сборки    |
| `down`            | Останавливает и удаляет запущенные контейнеры (`docker compose down`)                 |
| `clean`           | Останавливает сервисы и удаляет локальную копию репозитория CVAT                      |
| `createsuperuser` | Запускает команду внутри контейнера `cvat_server` для создания суперпользователя CVAT |

---

## Как использовать

```bash
cd "runners/CVAT_runner" # Переход в директорию с Makefile
```

```bash
make clone    # клонирует репозиторий, собирает образы и запускает сервисы
make build    # соберёт образ контейнера
make up       # запустит сервисы (с предварительной сборкой)
make down     # остановит и удалит контейнеры
make clean    # остановит сервисы и удалит папку с репозиторием
make createsuperuser # создаст суперпользователя внутри контейнера
```

---

## Смена порта на другой
Открываем файл docker-compose.yml

```
nano "runners/CVAT_runner/cvat/docker-compose.yml
```

Находим строку с портом 8080 и меняем этот внешний порт на свой
```
  traefik:
    image: traefik:v3.3
    container_name: traefik
    restart: always
    ports:
      - 8080:8080
      - 8090:8090
```

## Развёртка сервиса на платформе виртуализации proxmox

1. Устанавливаем Docker, [Docker compose](../docker_install.md)

2. Клонируем репозиторий

```
git clone https://github.com/cvat-ai/cvat
cd cvat
```

3. Устанавливаем переменную `CVAT_HOST` на наш внешний IP сервера  
```
export CVAT_HOST=External_IP_Address
```

4. Вводим следующую команду для фикса пропущенного порта, без которого приложение не развертывается  
```
docker compose down
docker run -d --rm --name cvat_opa_debug -p 8181:8181 openpolicyagent/opa:0.34.2-rootless \ run --server --set=decision_logs.console=true --set=services.cvat.url=http://host.docker.internal:7000/ \ --set=bundles.cvat.service=cvat --set=bundles.cvat.resource=/api/auth/rules
```

5. Поднимаем контейнер  
```
docker compose up -d
```

## Важно!

* После установки должно оставаться как минимум 10% свободного дискового пространства, иначе инструмент работать не будет.
* Для работы Makefile **необходимо**, чтобы на системе был установлен [docker и docker compose](../docker_install.md) и `make`.
* Для Windows необходимо запускать Makefile из Git Bash или WSL.
* Команда `createsuperuser` требует, чтобы сервисы CVAT были запущены.
