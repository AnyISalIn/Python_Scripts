import psutil
import arrow
import sys
import threading
from influxdb import InfluxDBClient
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s  - %(message)s')
host, port, dbname = '192.168.20.168', 8086, 'monitor-performance4'
hostname = os.uname()[1]

event = threading.Event()
client = InfluxDBClient(host, port, dbname)
client.switch_database(dbname)

def db_init():
    db_list = client.get_list_database()
    db_list = [ y for x in db_list for y in x.values() ]
    if dbname not in db_list:
        client.create_database(dbname)


def get_cpu():
    cpu_times = psutil.cpu_times()
    data = dict(zip(['user', 'nice', 'system', 'idle'], cpu_times))
    return data


def get_memory():
    mem_useage = psutil.virtual_memory()
    data = dict(zip(['total', 'available', 'percent', 'used', 'free', 'active', 'inactive', 'wired'], mem_useage))
    return data


def get_disk():
    result = {}
    disks = [ disk[1] for disk in psutil.disk_partitions() ]
    for item in disks:
        result[item] = dict(zip(['total', 'used', 'free', 'percent'], [ value for value in psutil.disk_usage(item) ]))
    return result


def get_network():
    net_ios = psutil.net_io_counters()
    net_ios_data = dict(zip(['bytes_sent', 'bytes_recv', 'packets_sent', 'packets_recv', 'errin', 'errout', 'dropin', 'dropout'], net_ios))
    return net_ios_data


def init_data(measurement, time, value, disk=None):
    return [
        {
            "measurement": measurement,
            "tags": {
                "host": hostname,
                "region": "us-west",
                "disk": disk
            },
            "time": time,
            "fields": value
        }
    ]


def send_data(measurement, time, value, disk=None):
    data = init_data(measurement, time, value, disk)
    logging.info(data)
    client.write_points(data)


def main():
    db_init()
    while not event.is_set():
        time = str(arrow.utcnow())
        all_item = [get_cpu, get_disk, get_memory, get_network]
        for item in all_item:
            item_name = item.__name__.strip('get_')
            if item != get_disk:
                send_data(item_name, time, item())
            else:
                for key, value in item().items():
                    send_data(item_name, time, value, key)

        event.wait(5)


if __name__ == '__main__':
    main()
