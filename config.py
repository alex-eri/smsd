modems = [
    '/dev/serial/by-id/usb-HUAWEI_Technology_HUAWEI_Mobile-if00-port0'
]

httpapis = [
    {
    'url': 'http://smspilot.ru/api.php',
    'data': 'apikey=134513451345&to={phone}&text={text}',
    'post': False
    }
]

port=8000
polling_port=8001

secret='secret'

