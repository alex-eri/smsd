Скопируй создай config.py:
```
#Модемы типа AT
modems = [...]

#Сервисы рассылок смс, запрос urlencoded
httpapis = [...]

#Порт для приёма смс к пересылке, urlencoded, GET или POST
port=8000

#Порт для стыковки для горизонтального масштабирования и подключения своих приложений
#HTTP long-polling, json
polling_port=8001

#Секрет, если указан, то требуется для отправки смсок, должен присутствовать в запросе. Если не указан, то не требуется.
secret='secret'
```


gsmmodem initially from https://github.com/faucamp/python-gsmmodem, modified for unicode and py3
