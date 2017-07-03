import logging
import os
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client


START_LIST = {
    '1704092e-abbf-4a56-873b-9b4aeb069945': 'dns',
    '6d08d7b0-1eec-4915-9665-e3ec217a98fc': 'webproxy',
    'e2cbf693-c9be-4b18-9720-3b68f8af164d': 'vanedisk-ext',
    'ce6b95a5-c275-45a3-9c54-5847642147d2': 'vanecloud-web',
    '8f080c3f-f4b5-4ee9-84a2-d8ec7745a447': 'ceilometer-mongo',
    '5fef0866-0ca3-45cf-9902-44dc7c4d0347': 'vanecloud-doc',
    'a65f01a3-536a-4ec9-933c-55f9b9a23d35': 'openvpn',
    '9ec42e11-3c1e-4ca6-bcd3-6bbbf0ec23af': 'vaneq-node1',
    '4b49c920-bc18-4576-bdd5-6de1b15ee971': 'vaneq-node2',
    'f6c1a3db-028d-46cd-b3ca-17d56325b33c': 'vaneq-node3',
    'ea5e75e0-e453-4483-bc62-1817a13f4799': 'vaneq-node4',
    '5fb567b2-5efe-4c69-8d00-30c8553084ff': 'windows-client',
    'c55d92cb-ddd9-4024-b753-cc1130e82bfa': 'proxy',
    '3148c657-90ba-4732-a628-def13c000f9a': 'repo'
}


# set logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# set nova client
auth = v3.Password(auth_url=os.getenv('OS_AUTH_URL'),
                   username=os.getenv('OS_USERNAME'),
                   password=os.getenv('OS_PASSWORD'),
                   project_name=os.getenv('OS_PROJECT_NAME'),
                   user_domain_id=os.getenv('OS_USER_DOMAIN_NAME'),
                   project_domain_id=os.getenv('OS_PROJECT_DOMAIN_NAME'))
s = session.Session(auth=auth)
nova = client.Client("2.1", session=s)

if __name__ == '__main__':
    servers = nova.servers.list(search_opts={'all_tenants': 1})

    for server in servers:
        if server.id in START_LIST:
            if server.status != 'ACTIVE':
                server.start()
                logger.info('{} START'.format(server.name))
            logger.info('{} STATUS IS {}, PASS'.format(
                server.name, server.status))
