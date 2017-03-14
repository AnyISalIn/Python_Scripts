import os
import json
from subprocess import Popen
from datetime import datetime, timedelta

LICENSE_ROOT = '/var/www/miq/vmdb/license/'
VANEQ_LIC_GEN = os.path.join(LICENSE_ROOT, 'vaneqLicGen.jar')
VANEQ_LIC_PUBLIC_KEY = os.path.join(LICENSE_ROOT, 'vaneq_pubkey.pub')


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
            json.dump(self._get_data(), out_file, indent=4)

    @property
    def _generate_cli(self):
        return ['/usr/bin/java', '-jar', VANEQ_LIC_GEN, VANEQ_LIC_PUBLIC_KEY, self.filename]

    def generate_license(self):
        self._write()
        Popen(self._generate_cli)


if __name__ == '__main__':
    GenerateVaneQLicense().generate_license()
