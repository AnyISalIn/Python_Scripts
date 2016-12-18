# Python_Scripts

本仓库中所有代码均在 `Python 3.5.2` 验证

## performance-monitor useage

这是一个简易的监控脚本 , 可以将数据存储到 `influxdb` 中.

```shellscript
$ python performance-monitor.py #使用时会将发送给 influxdb 的数据打印. 可以修改代码关闭.

2016-12-19 00:58:53,028 INFO  - [{'fields': {'nice': 0.0, 'idle': 780431.98, 'system': 23932.3, 'user': 37412.35}, 'time': '2016-12-18T16:58:53.028291+00:00', 'tags': {'region': 'us-west', 'disk': False, 'host': 'MacBook-Pro.local'
}, 'measurement': 'cpu'}]
2016-12-19 00:58:53,098 INFO  - [{'fields': {'total': 31645421568, 'percent': 97.0, 'used': 30452658176, 'free': 930619392}, 'time': '2016-12-18T16:58:53.028291+00:00', 'tags': {'region': 'us-west', 'disk': '/Volumes/ftp', 'host':
'MacBook-Pro.local'}, 'measurement': 'disk'}]
2016-12-19 00:58:53,138 INFO  - [{'fields': {'total': 31645421568, 'percent': 97.0, 'used': 30452658176, 'free': 930619392}, 'time': '2016-12-18T16:58:53.028291+00:00', 'tags': {'region': 'us-west', 'disk': '/Volumes/My Data', 'hos
t': 'MacBook-Pro.local'}, 'measurement': 'disk'}]
2016-12-19 00:58:53,201 INFO  - [{'fields': {'total': 31645421568, 'percent': 97.0, 'used': 30452658176, 'free': 930619392}, 'time': '2016-12-18T16:58:53.028291+00:00', 'tags': {'region': 'us-west', 'disk': '/', 'host': 'MacBook-Pr
o.local'}, 'measurement': 'disk'}]
2016-12-19 00:58:53,246 INFO  - [{'fields': {'total': 31645421568, 'percent': 97.0, 'used': 30452658176, 'free': 930619392}, 'time': '2016-12-18T16:58:53.028291+00:00', 'tags': {'region': 'us-west', 'disk': '/Volumes/Untitled', 'ho
st': 'MacBook-Pro.local'}, 'measurement': 'disk'}]
2016-12-19 00:58:53,274 INFO  - [{'fields': {'total': 17179869184, 'active': 9035608064, 'available': 5725958144, 'wired': 1949495296, 'inactive': 5535584256, 'percent': 66.7, 'used': 16520687616, 'free': 190373888}, 'time': '2016-
12-18T16:58:53.028291+00:00', 'tags': {'region': 'us-west', 'disk': False, 'host': 'MacBook-Pro.local'}, 'measurement': 'memory'}]
2016-12-19 00:58:53,305 INFO  - [{'fields': {'dropout': 0, 'packets_sent': 2755297, 'errin': 0, 'bytes_sent': 1042639076, 'packets_recv': 3622496, 'errout': 0, 'bytes_recv': 3038254885, 'dropin': 0}, 'time': '2016-12-18T16:58:53.02
8291+00:00', 'tags': {'region': 'us-west', 'disk': False, 'host': 'MacBook-Pro.local'}, 'measurement': 'network'}]
```
