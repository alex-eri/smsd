Хуавэй

пример запроса POST http://192.168.8.1/api/sms/send-sms

```
<?xml version="1.0" encoding="UTF-8"?><request><Index>-1</Index><Phones><Phone>+7123456789</Phone></Phones><Sca></Sca><Content>Прив!</Content><Length>5</Length><Reserved>0</Reserved><Date>2016-06-12 22:56:44</Date></request>
```

ответ
```
OK
```

ZTE
пример запроса POST http://192.168.0.1/goform/goform_set_cmd_process
```
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
```
```
isTest=false&goformId=SEND_SMS&notCallback=true&Number=%2B79158327039&sms_time=16%3B06%3B12%3B23%3B03%3B03%3B%2B3&MessageBody=041F04400438043204350442&ID=-1&encode_type=UNICODE
Name	
```
Ответ
```
{"result":"success"}
```
