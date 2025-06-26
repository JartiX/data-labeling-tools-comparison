# Настройка хранения данных в облаке Google Cloud/OwnCloud (Linux)

## 1. Настроить локальное хранение данных CVAT по [этой документации](./local_data_contain.md)

## 2. Переименовать папку data в temp  
> Перед этим остановить контейнер если был запущен  
```
docker compose down
```

```
mv ./data ./temp
```

## 3. Установить rclone

```
sudo apt install rclone
```

## 4. Создаем проект и получаем Client ID, Client Secret для Google Cloud

### 4.1 Перейти в [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

### 4.1 Создать проект, если его еще нет

![](../../imgs/google%20cloud/main_cloud_page.png)

### 4.2 Найти и включить Google Drive API 
> (API & Services → Library → Google Drive API → Enable)

![](../../imgs/google%20cloud/find_api_google.png)
![](../../imgs/google%20cloud/enable_api_google.png)

### 4.3 Перейти в Credentials → Create Credentials

![](../../imgs/google%20cloud/create_credentials.png)

### 4.4 Выбрать User data

![](../../imgs/google%20cloud/create_credentials_1.png)

### 4.5 Дать имя проекту, вписать свою почту в два поля
![](../../imgs/google%20cloud/create_credentials_2.png)


### 4.6 Выбрать тип приложения Desktop App и дать ему название
![](../../imgs/google%20cloud/create_credentials_3.png)

### 4.7 Скачать JSON с Client ID, Client Secret

### 4.8 Добавить себя в тестировщики приложения. Нажать Oauth consent screen

![](../../imgs/google%20cloud/oauth_consent.png)

### 4.9 Добавить себя в Test Users (по email)

![](../../imgs/google%20cloud/test_user.png)

# 5. Подключить google cloud/Owncloud по [этой документации](./connect_cloud.md)

# 6. Монтируем локальную папку с облаком

## 1 Способ: Простой фоновый запуск с логированием в ~/rclone.log
```
nohup rclone mount <REMOTE-NAME>:CVAT_data /PATH/TO/data --vfs-cache-mode full --allow-other --daemon &> ~/rclone.log &
```  
> Чтобы остановить, узнаем PID и убьем процесс
```
ps aux | grep rclone
kill <PID>
```

## 2 Способ: Автозапуск через systemd

### 1. Создать файл сервис
```
sudo nano /etc/systemd/system/rclone-cvat.mount.service
```

### 2. Внести в него следующее содержимое (User, REMOTE и путь до date заменить на свои):
```
[Unit]
Description=Mount Cloud for CVAT
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/rclone mount <REMOTE-NAME>:CVAT_data /PATH/TO/data \
  --vfs-cache-mode full \
  --allow-other \
  --dir-cache-time 12h \
  --log-file /PATH/TO/CVAT/rclone-cvat.log \
  --log-level INFO

Restart=on-failure
User=<YOUR-USER-NAME>

[Install]
WantedBy=multi-user.target
```

### 3. Дать доступ на редактирование всем пользователям
> Нужно раскомментировать строку #user_allow_other
```
sudo nano /etc/fuse.conf
```

### 4. Ввести следующие команды
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable rclone-cvat.mount.service
sudo systemctl start rclone-cvat.mount.service
```  
> Проверка `systemctl status rclone-cvat.mount.service`

> После монтирования диска подождать около 3 минут перед следующими действиями

# 16. Вернуть данные с temp в data
```
cp -r ./temp/. ./data/
rm -rf ./temp
```

# 17. Запустить докер образ

```
docker compose up -d
```