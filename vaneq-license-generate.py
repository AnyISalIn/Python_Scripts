import os
import json
import argparse
from subprocess import Popen
from datetime import datetime, timedelta
from uuid import getnode, uuid4
from copy import deepcopy
from itsdangerous import JSONWebSignatureSerializer as Serializer

LICENSE_ROOT = '/var/www/miq/vmdb/license/'
VANEQ_LIC_GEN = os.path.join(LICENSE_ROOT, 'vaneqLicGen.jar')
VANEQ_LIC_PUBLIC_KEY = os.path.join(LICENSE_ROOT, 'vaneq_pubkey.pub')
VANEQ_LIC_MAC_UUID = os.path.join(LICENSE_ROOT, 'mac_uuid')
VANEQ_LIC_FILE = os.path.join(LICENSE_ROOT, 'vaneQLic')
s = Serializer('vaneq+1s', salt='vaneq+2s')

parser = argparse.ArgumentParser(prog='license generate')
parser.add_argument('-g', '--gen', dest='gen', help='gen info', default=False, action='store_true')
parser.add_argument('-l', '--license', dest='license', help='generate license', default=False, action='store_true')
parser.add_argument('-d', '--decrypt', dest='encrypt_data', help='decrypt data', default=None)
args = parser.parse_args()


class GenerateVaneQLicense(object):
    def __init__(self, lic_generate_date=None, client_name='CSHO-test',
                 lic_valid_date=None, client_mac_addresses=None, lic_vm_number=50,
                 client_system_uuids=None, filename='vaneqLicContent'):
        if lic_generate_date is None:
            self.lic_generate_date = self._format_date(datetime.now())

        if lic_valid_date is None:
            self.lic_valid_date = self._format_date(
                datetime.now() + timedelta(days=30))

        if client_mac_addresses is None:
            self.client_mac_addresses = []

        if client_system_uuids is None:
            self.client_system_uuids = []

        self.client_name = client_name
        self.lic_vm_number = lic_vm_number
        self.filename = os.path.abspath(os.path.join('', filename))

    def _format_date(self, time):
        return datetime.strftime(time, '%Y-%m-%d')

    def _get_data(self):
        return {
            "lic_generate_date": self.lic_generate_date,
            "client_name": self.client_name,
            "lic_valid_date": self.lic_valid_date,
            "client_mac_addresses": self.client_mac_addresses,
            "lic_vm_number": self.lic_vm_number,
            "client_system_uuids": self.client_system_uuids
        }

    def _write(self):
        with open(self.filename, 'w') as out_file:
            json.dump(self._generate_content(), out_file, indent=4)

    @property
    def _generate_cli(self):
        return ['/usr/bin/java', '-jar', VANEQ_LIC_GEN, VANEQ_LIC_PUBLIC_KEY, self.filename]

    @property
    def _get_mac(self):
        return ':'.join(("%012X" % getnode())[i:i + 2] for i in range(0, 12, 2))

    @property
    def _get_uuid(self):
        return str(uuid4())

    def generate_license(self):
        self._write()
        if os.path.isfile(VANEQ_LIC_FILE):
            os.remove(VANEQ_LIC_FILE)
        Popen(self._generate_cli)

    def _generate_content(self):
        data = deepcopy(self._get_data())
        with open(VANEQ_LIC_MAC_UUID, 'r') as f:
            d = json.load(f)
            vaneq_mac = str(d['mac'])
            vaneq_uuid = str(d['uuid'])
        data['client_mac_addresses'].append({'client_mac_addr': vaneq_mac})
        data['client_system_uuids'].append({'client_system_uuid': vaneq_uuid})
        return data

    def generate_encrypt_content(self):
        return s.dumps(self._generate_content())

    def generate_mac_uuid(self):
        data = {}
        data['mac'] = self._get_mac
        data['uuid'] = self._get_uuid
        with open(VANEQ_LIC_MAC_UUID, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def decrypt_content(data):
        return s.loads(data)


if __name__ == '__main__':
    g = GenerateVaneQLicense()
    if args.gen:
        print(g.generate_encrypt_content())
    if args.license:
        if not os.path.isfile(VANEQ_LIC_MAC_UUID):
            g.generate_mac_uuid()
        g.generate_license()
    if args.encrypt_data is not None:
        print(json.dumps(g.decrypt_content(args.encrypt_data), indent=4))
