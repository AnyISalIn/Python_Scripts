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
        parse_pids = get_childrens(main_pid)
        parse_pids.append(main_pid)
        for pid in parse_pids:
            process_info = psutil.Process(pid)
            if pid == main_pid:
                worker_name = 'MIQ Server'
            else:
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
        worker_count = data['worker_count']
        for key, value in worker_count.items():
            worker_name = key.replace('.', '_')
            worker_count = value
            uni_data = '.'.join(['worker_count', worker_name])
            g.send(uni_data, value)
            logging.info('Send {} ==> {} success'.format(uni_data, value))
    else:
        woker_info = data['worker_info']
        for key, value in woker_info.items():
            if key == 'worker_name':
                worker_name = woker_info['worker_name'].replace('.', '_')
            elif key == 'memory_used':
                memory_used = str(woker_info['memory_used'])
            else:
                pid = str(woker_info['pid'])
        uni_data = '.'.join(['worker_info', worker_name, pid])
        g.send(uni_data, memory_used)
        logging.info('Send {} ==> {} success'.format(uni_data, memory_used))


def main():
    for p in psutil.process_iter():
        if 'MIQ Server' in  p.cmdline():
            main_pid = p.pid
    for line in parse(main_pid):
        send(line)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        event.is_set()
