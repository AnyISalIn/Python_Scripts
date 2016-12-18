# Python_Scripts

本仓库中所有代码均在 `Python 3.5.2` 验证

## performance-monitor usage

这是一个简易的监控脚本 , 可以将数据存储到 `influxdb` 中.

```shellscript
$ python performance-monitor.py #使用时会将发送给 influxdb 的数据打印. 可以修改代码关闭.

2016-12-19 07:54:43,979 INFO  - [{'measurement': 'memory', 'time': '2016-12-18T23:54:43.258035+00:00', 'tags': {'region': 'us-west', 'disk': None, 'host': 'MacBook-Pro.local'}, 'fields': {'total': 17179869184, 'inactive': 4581322752, 'available': 5093101568, 'active': 9624330240, 'used': 16166903808, 'wired': 1961250816, 'free': 511778816, 'percent': 70.4}}]
2016-12-19 07:54:44,038 INFO  - [{'measurement': 'network', 'time': '2016-12-18T23:54:43.258035+00:00', 'tags': {'region': 'us-west', 'disk': None, 'host': 'MacBook-Pro.local'}, 'fields': {'packets_recv': 3887002, 'bytes_recv': 3096850918, 'packets_sent': 3062658, 'dropout': 0, 'dropin': 0, 'errout': 0, 'bytes_sent': 1103373801, 'errin': 0}}]
2016-12-19 07:54:49,626 INFO  - [{'measurement': 'cpu', 'time': '2016-12-18T23:54:49.625942+00:00', 'tags': {'region': 'us-west', 'disk': None, 'host': 'MacBook-Pro.local'}, 'fields': {'idle': 974277.24, 'nice': 0.0, 'user': 40822.26, 'system': 26323.14}}]
2016-12-19 07:54:50,049 INFO  - [{'measurement': 'disk', 'time': '2016-12-18T23:54:49.625942+00:00', 'tags': {'region': 'us-west', 'disk': '/Volumes/ftp', 'host': 'MacBook-Pro.local'}, 'fields': {'used': 33304731648, 'percent': 77.5, 'free': 9646735360, 'total': 42951467008}}]
2016-12-19 07:54:50,111 INFO  - [{'measurement': 'disk', 'time': '2016-12-18T23:54:49.625942+00:00', 'tags': {'region': 'us-west', 'disk': '/Volumes/Untitled', 'host': 'MacBook-Pro.local'}, 'fields': {'used': 89772699648, 'percent': 95.0, 'free': 4681207808, 'total': 94453907456}}]
2016-12-19 07:54:50,152 INFO  - [{'measurement': 'disk', 'time': '2016-12-18T23:54:49.625942+00:00', 'tags': {'region': 'us-west', 'disk': '/Volumes/My Data', 'host': 'MacBook-Pro.local'}, 'fields': {'used': 650238570496, 'percent': 67.9, 'free': 307013795840, 'total': 957252366336}}]
2016-12-19 07:54:50,195 INFO  - [{'measurement': 'disk', 'time': '2016-12-18T23:54:49.625942+00:00', 'tags': {'region': 'us-west', 'disk': '/', 'host': 'MacBook-Pro.local'}, 'fields': {'used': 30317142016, 'percent': 96.6, 'free': 1066135552, 'total': 31645421568}}]
2016-12-19 07:54:50,244 INFO  - [{'measurement': 'memory', 'time': '2016-12-18T23:54:49.625942+00:00', 'tags': {'region': 'us-west', 'disk': None, 'host': 'MacBook-Pro.local'}, 'fields': {'total': 17179869184, 'inactive': 4585308160, 'available': 5112082432, 'active': 9579761664, 'used': 16147304448, 'wired': 1982234624, 'free': 526774272, 'percent': 70.2}}]
2016-12-19 07:54:50,312 INFO  - [{'measurement': 'network', 'time': '2016-12-18T23:54:49.625942+00:00', 'tags': {'region': 'us-west', 'disk': None, 'host': 'MacBook-Pro.local'}, 'fields': {'packets_recv': 3887114, 'bytes_recv': 3096870775, 'packets_sent': 3062787, 'dropout': 0, 'dropin': 0, 'errout': 0, 'bytes_sent': 1103402125, 'errin': 0}}]
```
