import psycopg2
import graphitesend
import threading
import logging
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from datetime import timedelta

event = threading.Event()
g = graphitesend.init(prefix='server_status', graphite_server='localhost', system_name='')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s  - %(message)s')


class GetVaneQServersInfo:
    def __init__(self, **kwargs):
        self.pool = SimpleConnectionPool(minconn=2, maxconn=5, **kwargs)
        self.filter_item = ['name', 'mac_address', 'version', 'capabilities',
                            'drb_uri', 'ipaddress', 'upgrade_message', 'build', 'guid']

    def _get_data(self, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM miq_servers')
            result = cur.fetchall()
        return result

    def _parse_data(self, conn):
        while not event.is_set():
            data = self._get_data(conn)
            result = {}
            for server in data:
                hostname = server.pop('hostname')
                for item in self.filter_item:
                    server.pop(item)

                for key, value in server.items():
                    new_key = '{}.{}'.format(hostname, key)
                    if value is None or value is False:
                        result[new_key] = 0
                        continue
                    elif value is True:
                        result[new_key] = 1
                        continue


                    if key in ('last_heartbeat', 'started_on',
                               'stopped_on', 'last_update_check'):
                        result[new_key] = (value + timedelta(hours=8)).strftime('%Y%m%d%H%M')
                    elif key in ('memory_size', 'memory_usage',
                                 'proportional_set_size'):
                        result[new_key] = int(value)
                    elif key == 'status':
                        if value == 'started':
                            result[new_key] = 1
                        else:
                            result[new_key] = 0
                    else:
                        result[new_key] = str(value)
            yield result

    def _send_data(self, data):
        g.send_dict(data)

    def main(self):
        while not event.is_set():
            conn = self.pool.getconn()
            for data in self._parse_data(conn):
                self._send_data(data)
                logging.info(data)
                event.wait(5)


if __name__ == '__main__':
    try:
        q = GetVaneQServersInfo(host='192.168.20.103',
                                port=5432,
                                user='root',
                                password='smartvm',
                                database='vmdb_production')
        q.main()
    except KeyboardInterrupt:
        event.is_set()
