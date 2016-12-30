import docker
import logging

# This is get hash image mapping example
# mapping = {}
# for i in all_images:
#     f_tags = i['RepoTags'][:]
#     for f_tag in f_tags:
#         if f_tag.startswith('gcr') or f_tag.startswith('quay') or f_tag.startswith('docker'):
#             key = i['Id']
#             value = f_tag
#             mapping[key] = value


client = docker.from_env()
client.version() #inspect client api version, if not ok, exit

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s  - %(message)s')

hash_image_map = {
     u'sha256:116cad037a5d7ff69a85243a0884b346c91775803923e24f22a73c13d3409b68': u'quay.io/deis/fluentd:v2.5.0',
     u'sha256:26b19186b7d957d852fb3e8148c4cf7abe2bce0dd2890edc6157c1c9c2dc8994': u'quay.io/deis/registry-proxy:v1.1.1',
     u'sha256:26cf1ed9b14486b93acd70c060a17fea13620393d3aa8e76036b773197c47a05': u'gcr.io/google_containers/kubedns-amd64:1.9',
     u'sha256:390c5e1c3ebdd861471e82ae7bc1e6e51645e77a7f720d56a841173a2c189e2d': u'quay.io/deis/nsq:v2.2.5',
     u'sha256:3ec65756a89b70b4095e43a340a6e2d5696cac7a93a29619ff5c4b6be9af2773': u'gcr.io/google_containers/kube-dnsmasq-amd64:1.4',
     u'sha256:5271aabced07deae353277e2b8bd5b2e30ddb0b4a5884a5940115881ea8753ef': u'gcr.io/google_containers/dnsmasq-metrics-amd64:1.0',
     u'sha256:6506e7b74dacef20aee5deee412374093514cc3aec10f84df01f0e55ea85ac2c': u'gcr.io/google_containers/kube-scheduler-amd64:v1.5.1',
     u'sha256:71d2b27b03f6cd127b54f3c49616db4819e4a2e3c16e74b3140c8b9fbcbb82b5': u'gcr.io/google_containers/kube-proxy-amd64:v1.5.1',
     u'sha256:856e39ac7be33be8e2038cff52a90a23924ef149dafab7dada05d6d485ff9fbf': u'gcr.io/google_containers/etcd-amd64:3.0.14-kubeadm',
     u'sha256:8c12509df629179f22653082cd3348b92e69a2cb953e8ee39a3c7cbd890ba309': u'gcr.io/google_containers/kube-apiserver-amd64:v1.5.1',
     u'sha256:93a43bfb39bfe9795e76ccd75d7a0e6d40e2ae8563456a2a77c1b4cfc3bbd967': u'gcr.io/google_containers/exechealthz-amd64:1.2',
     u'sha256:99e59f495ffaa222bfeb67580213e8c28c1e885f1d245ab2bbe3b1b1ec3bd0b2': u'gcr.io/google_containers/pause-amd64:3.0',
     u'sha256:c5e0c9a457fcb53ac5c564656f3fabba733ab1e8187e98d095c88356b9245de8': u'gcr.io/google_containers/kube-discovery-amd64:1.0',
     u'sha256:cd568403172042ef00c7a48389d9862c1edaeac00c6cae510cf0e7549aba34bd': u'gcr.io/google_containers/kube-controller-manager-amd64:v1.5.1',
     u'sha256:f145fa7f4157f83a29eaa6e9134e7bc502a453f2fd82095a02dbf608ca331536': u'quay.io/deis/telegraf:v2.7.0',
     u'sha256:a4740ae55aae4985e19624fe18a49455ca386da6a7918723d13b7672a3474082': u'docker.io/weaveworks/weave-kube:1.8.2',
     u'sha256:c91ef3f4642b6e3bc033a516808d34409bfce57962e1ec506c23fde0b8275fa3': u'docker.io/weaveworks/weave-npc:1.8.2'
 }

pull_images = [
     'harbor.vanecloud.com/google_containers/kube-scheduler-amd64:v1.5.1',
     'harbor.vanecloud.com/deis/fluentd:v2.5.0',
     'harbor.vanecloud.com/deis/nsq:v2.2.5',
     'harbor.vanecloud.com/google_containers/kube-dnsmasq-amd64:1.4',
     'harbor.vanecloud.com/weaveworks/weave-kube:1.8.2',
     'harbor.vanecloud.com/weaveworks/weave-npc:1.8.2',
     'harbor.vanecloud.com/google_containers/dnsmasq-metrics-amd64:1.0',
     'harbor.vanecloud.com/google_containers/kube-proxy-amd64:v1.5.1',
     'harbor.vanecloud.com/google_containers/etcd-amd64:3.0.14-kubeadm',
     'harbor.vanecloud.com/library/kube-apiserver-amd64:v1.5.1',
     'harbor.vanecloud.com/google_containers/pause-amd64:3.0',
     'harbor.vanecloud.com/deis/registry-proxy:v1.1.1',
     'harbor.vanecloud.com/google_containers/kube-discovery-amd64:1.0',
     'harbor.vanecloud.com/google_containers/kube-controller-manager-amd64:v1.5.1',
     'harbor.vanecloud.com/google_containers/kubedns-amd64:1.9',
     'harbor.vanecloud.com/deis/telegraf:v2.7.0'
 ]



def pull_image(image):
    logging.info('start pull {}'.format(image))
    geted_image = client.images.pull(image)
    if geted_image:
        logging.info('{} pull success'.format(image))
        return geted_image


def handle(image_obj):
    image_tag = hash_image_map.get(image_obj.id)
    if image_tag:
        image_tag = str(image_tag)
        repository, tag = image_tag.split(':')
        image_obj.tag(repository, tag)
        logging.info('{} tagged success'.format(image_tag))
    else:
        logging.error('{} not in hash map'.format(str(image_obj.tags[0])))


def main():
    for image in pull_images:
        geted_image = pull_image(image)
        handle(geted_image)
    logging.info('All Item is Finished, Fuck GFW !!!!')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
