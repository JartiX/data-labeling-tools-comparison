# Настройка хранения данных в облаке Google Cloud (Linux)

## 1. Настроить локальное хранение данных CVAT по [этой документации](./local_data_contain.md)

## 2. Переименовать папку data в temp  
> Перед этим остановить контейнер если был запущен  
```
docker compose down
```

```
mv -r ./data ./temp
```

## 3. Установить rclone

```
sudo apt install rclone
```

# 4. Перейти в [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

# 5. Создать проект, если его еще нет

![](../../imgs/google%20cloud/main_cloud_page.png)

# 6. Найти и включить Google Drive API 
> (API & Services → Library → Google Drive API → Enable)

![](../../imgs/google%20cloud/find_api_google.png)
![](../../imgs/google%20cloud/enable_api_google.png)

# 7. Перейти в Credentials → Create Credentials

![](../../imgs/google%20cloud/create_credentials.png)

# 8. Выбрать User data

![](../../imgs/google%20cloud/create_credentials_1.png)

# 9. Дать имя проекту, вписать свою почту в два поля
![](../../imgs/google%20cloud/create_credentials_2.png)


# 10. Выбрать тип приложения Desktop App и дать ему название
![](../../imgs/google%20cloud/create_credentials_3.png)

# 11. Скачать JSON с Client ID, Client Secret

# 12. Добавить себя в тестировщики приложения. Нажать Oauth consent screen

![](../../imgs/google%20cloud/oauth_consent.png)

# 13. Добавить себя в Test Users (по email)

![](../../imgs/google%20cloud/test_user.png)

# 14. Связать google cloud и локальное хранилище

```
rclone config
```
## 14.1 Выбираем n
```
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
```

## 14.2 Даем название удаленному хранилищу
```
Enter name for new remote.
name> gdrive
```

## 14.3 Выбираем номер с Google Drive
```
Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.

Storage> 18
```

## 14.4 Вводим Client id
```
Option client_id.
Google Application Client Id
Setting your own is recommended.
See https://rclone.org/drive/#making-your-own-client-id for how to create your own.
If you leave this blank, it will use an internal key which is low performance.
Enter a value. Press Enter to leave empty.
client_id> Your-Client-Id
```

## 14.5 Вводим Client Secret
```
Option client_secret.
OAuth Client Secret.
Leave blank normally.
Enter a value. Press Enter to leave empty.
client_secret> Your-Client-Secret
```

## 14.6 Выбираем права доступа
```
Option scope.
Scope that rclone should use when requesting access from drive.
Choose a number from below, or type in your own value.
Press Enter to leave empty.

scope> 1
```

## 14.7  Пропускаем
```
Option service_account_file.
Service Account Credentials JSON file path.
Leave blank normally.
Needed only if you want use SA instead of interactive login.
Leading `~` will be expanded in the file name as will environment variables such as `${RCLONE_CONFIG_DIR}`.
Enter a value. Press Enter to leave empty.
service_account_file>
```

## 14.8 Не меняем доп. настройки
```
Edit advanced config?
y) Yes
n) No (default)
y/n> n
```

## 14.9 Не используем автоконфиг
```
Use auto config?
 * Say Y if not sure
 * Say N if you are working on a remote or headless machine

y) Yes (default)
n) No
y/n> n
```

## 14.10 Копируем предложенную команду и запускаем её на устройсте с браузером
```
Option config_token.
For this to work, you will need rclone available on a machine that has
a web browser available.
For more help and alternate methods see: https://rclone.org/remote_setup/
Execute the following on the machine with the web browser (same rclone
version recommended):
        rclone authorize "drive" "<HASH>"
Then paste the result.
Enter a value.
config_token> <YOUR-CONFIG-TOKEN>
```  
> После ввода предложенной команды переходим по ссылке из терминала и авторизируемся с аккаунта, который указали как test user, после этого вернуться в консоли появится нужный нам ключ

## 14.11 Если обычный диск, выбираем **n**, если корпоративный/командный, выбираем **y**
```
Configure this as a Shared Drive (Team Drive)?

y) Yes
n) No (default)
y/n> n
```

## 14.12 Сохраняем
```
Keep this "<REMOTE-NAME>" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y
```

## 14.13 Монтируем локальную папку с Google Drive

### 1 Способ: Простой фоновый запуск с логированием в ~/rclone.log
```
nohup rclone mount <REMOTE-NAME>:CVAT_data /home/jartix/cvat/data --vfs-cache-mode full --allow-other --daemon &> ~/rclone.log &
```  
> Чтобы остановить, узнаем PID и убьем процесс
```
ps aux | grep rclone
kill <PID>
```

### 2 Способ: Автозапуск через systemd

#### 1. Создать файл сервис
```
sudo nano /etc/systemd/system/rclone-cvat.mount.service
```

#### 2. Внести в него следующее содержимое (User, REMOTE и путь до date заменить на свои):
```
[Unit]
Description=Mount Google Drive for CVAT
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

#### 3. Ввести следующие команды
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable rclone-cvat.mount.service
sudo systemctl start rclone-cvat.mount.service
```  
> Проверка `systemctl status rclone-cvat.mount.service`

> После монтирования диска подождать около 3 минут перед следующими действиями

# 15. Вернуть данные с temp в data
```
cp -r ./temp/. ./data/
rm -rf ./temp
```

# 16. Запустить докер образ

```
docker compose up -d
```