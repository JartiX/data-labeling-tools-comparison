# В документации прописаны только консольные команды docker которыми можно развернуть образ, используя их напишу docker compose которым можно будет быстро и легко запускать label studio

# Ошибка порта

Указав стандартный порт, получаю ошибку, так как этот порт уже занят CVAT

```
Error response from daemon: driver failed programming external connectivity on endpoint label-studio (eb4e2c27137a5ca146e6343e6d1b9a01514623fb7ab1ccb12f275c21069951e4): Bind for 0.0.0.0:8080 failed: port is already allocated
```

Меняю стандартный порт в docker compose на 8081