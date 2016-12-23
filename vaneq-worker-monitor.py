import psutil
import sys
import threading
import re
import graphitesend
import logging



event = threading.Event()
pattern = r'(?P<name>.*) (id|\(tcp).*'
o = re.compile(pattern)
g = graphitesend.init(graphite_server='localhost')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s  - %(message)s')


def get_childrens(main_pid):
    childrens = psutil.Process(main_pid).children()
    children_pids = [ x.pid for x in childrens ]
    return children_pids


def parse(main_pid):
    while not event.is_set():
        count = {}
        children_pids = get_childrens(main_pid)
        for pid in children_pids:
            process_info = psutil.Process(pid)
            worker_name = o.search(process_info.cmdline()[0]).groupdict()['name']
            if worker_name not in count.keys():
                count[worker_name] = 0
            count[worker_name] += 1
            agg = dict(zip(['worker_name', 'pid', 'memory_used'], [worker_name, pid, process_info.memory_info().rss]))
            yield {'worker_info': agg}
        yield {'worker_count': count}
        event.wait(5)


def send(data):
    if 'worker_count' in data.keys():
        for key, value in data['worker_count'].items():
            g.send(key, value)
    else:
        # g = graphitesend.init(graphite_server='localhost', group='worker_info')
        # for
        pass


def main():
    for line in parse(int(sys.argv[1])):
        send(line)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        event.is_set()
