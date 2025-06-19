# API Endpoints

# [Полная документация по API](https://api.labelstud.io/api-reference/api-reference/) 
## Чтобы обратиться к API нужен API-токен

## Создание токена:

1. Создать токен в личном кабинете и скопировать его
![token](../../imgs/api%20token.png)

2. Отправить POST запрос на точку API `/api/token/refresh`, в теле запроса передать  ```{
  "refresh": "your-api-token"
}``` В ответ получим Bearer токен который понадобится во всех обращениях к API

3. Далее во всех последующих обращениях к API в Header запроса передавать параметр "Authorization: Bearer \<token\>"

## Основные конечные точки API

1. Получить аннотацию по ID:  
GET `/api/annotations/{id}`  
Возвращает аннотацию в таком виде:  
```
{
    "id": 1,
    "result": [
        {
            "original_width": 148,
            "original_height": 137,
            "image_rotation": 0,
            "value": {
                "x": 18.750866179702726,
                "y": 12.564102313300662,
                "width": 63.491857363851814,
                "height": 71.15384635448774,
                "rotation": 0,
                "rectanglelabels": [
                    "road sign"
                ]
            },
            "id": "Uy5L2T0k5z",
            "from_name": "label",
            "to_name": "image",
            "type": "rectanglelabels",
            "origin": "manual"
        }
    ],
    "created_username": " artem@gmail.com, 1",
    "created_ago": "2 hours, 1 minute",
    "completed_by": 1,
    "was_cancelled": false,
    "ground_truth": false,
    "created_at": "2025-06-19T11:17:01.890397Z",
    "updated_at": "2025-06-19T11:17:01.890439Z",
    "draft_created_at": "2025-06-19T11:15:59.693721Z",
    "lead_time": 75.529,
    "import_id": null,
    "last_action": null,
    "bulk_created": false,
    "task": 1,
    "project": 3,
    "updated_by": 1,
    "parent_prediction": null,
    "parent_annotation": null,
    "last_created_by": null
}
```

2. Создать новый проект  
POST `/api/projects`  
Пример тела запроса: ```{
  "title": "Sentiment Project",
  "label_config": "<View><Text name=\"text\" value=\"$text\"/><Choices name=\"sentiment\" toName=\"text\"><Choice value=\"Positive\"/><Choice value=\"Negative\"/></Choices></View>"
}```

3. Получить список проектов:  
GET `/api/projects`  

4. Импорт датасета в проект:  
POST `/api/projects/{id}/import`  
Возможное тело запроса:  
```
[
  {"text": "Great service!"},
  {"text": "Not satisfied with the product."}
]
```  

5. Экспорт проекта в JSON:
GET `/api/projects/{id}/export?exportType=JSON`  
