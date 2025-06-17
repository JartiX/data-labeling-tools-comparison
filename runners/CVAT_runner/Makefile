REPO_URL = https://github.com/cvat-ai/cvat.git
REPO_DIR = cvat

.PHONY: all clone build up down clean

all: up

# Клонирование репозитория если он не существует
clone:
	if [ ! -d "$(REPO_DIR)" ]; then \
		git clone $(REPO_URL); \
	fi

# Сборка контейнеров
build: clone
	cd $(REPO_DIR) && docker compose build

# Запуск контейнеров
up: build
	cd $(REPO_DIR) && docker compose up -d

# Остановка контейнеров
down:
	cd $(REPO_DIR) && docker compose down

# Создание суперпользователя
createsuperuser:
	cd $(REPO_DIR) && docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'

# Очистка — удаление репозитория
clean: down
	rm -rf $(REPO_DIR)
