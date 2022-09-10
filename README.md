### Установка

1. Создание виртуального окружения и установка зависимостей:
```commandline
poetry install
```

2. Активация виртуального окружения:

```commandline
poetry shell
```


### Запуск

0. Создание `.env` файла с необходимыми переменными:
```commandline
make env
```

1. Запуск сервера nats:
```commandline
make nats
```

3. Запуск приложения:
```commandline
make run
```
