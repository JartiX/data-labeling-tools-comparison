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

## 3. Установить google-drive-ocalmfuse

```
sudo add-apt-repository ppa:alessandro-strada/ppa
sudo apt-get update
sudo apt-get install google-drive-ocamlfuse
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

> Появится ссылка, по ней нужно будет перейти и авторизироваться с аккаунта, который указали как test user, после этого из адресной строки достать значение code и вписать его в консоль
```
google-drive-ocamlfuse -id "CLIENT_ID" -secret "CLIENT_SECRET" -headless data
```

# 15. Вернуть данные с temp в data
```
cp -r ./temp/. ./data/
rm -rf ./temp
```

# 16. Запустить докер образ

```
docker compose up -d
```