from .apiclient import ApiClient
import sys
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64

class PrismAuthenticate(ApiClient):

    def __init__(self, cluster_ip, username, password):

        self.cluster_ip = cluster_ip
        self.username = username
        self.password = password
        self.cookie = None

        self.method = 'post'
        self.cluster_ip = cluster_ip
        self.username = username
        self.password = password
        self.verify = True
        self.base_url = "https://{}:9440/api/nutanix/v3".format(self.cluster_ip)
        self.entity_type = 'clusters/list'
        self.request_url = "{}/{}".format(self.base_url, self.entity_type)
        self.body = '{}'

    def verify_ssl(self, value=True):
        self.verify = value

    def set_pc_request(self):
        self.method = 'post'
        self.base_url = "https://{}:9440/api/nutanix/v3".format(self.cluster_ip)
        self.entity_type = 'clusters/list'
        self.request_url = "{}/{}".format(self.base_url, self.entity_type)

    def get_cookie(self):

        self.set_pc_request()
        result = self.get_info(return_json=False)
        self.cookie = result.headers['Set-Cookie']
        return self.cookie


class KarbonClient:

    def __init__(self, cluster_ip, cookie, verify=True):
        self.method = 'post'
        self.cluster_ip = cluster_ip
        self.verify = verify
        self.base_url = "https://{}:7050/acs/k8s".format(self.cluster_ip)
        self.entity_type = 'cluster/list'
        self.request_url = "{}/{}".format(self.base_url, self.entity_type)
        self.body = '{}'
        self.cookie = cookie

    def get_info(self, return_json=True, cookie=''):

        if not self.verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        headers = {'Content-Type': 'application/json; charset=utf-8', 'Cookie': cookie}

        try:
            if (self.method == 'post'):
                r = requests.post(self.request_url, data=self.body, verify=self.verify, headers=headers, timeout=60)
            else:
                r = requests.get(self.request_url, verify=self.verify, headers=headers, timeout=60)
        except requests.ConnectTimeout:
            print(
                'Connection timed out while connecting to {}. Please check your connection, then try again.'.format(
                    self.cluster_ip))
            sys.exit()
        except requests.ConnectionError:
            print('An error occurred while connecting to {}. Please check your connection, then try again.'.format(
                self.cluster_ip))
            sys.exit()
        except requests.HTTPError:
            print(
                'An HTTP error occurred while connecting to {}. Please check your connection, then try again.'.format(
                    self.cluster_ip))
            sys.exit()

        if r.status_code >= 500:
            print('An HTTP server error has occurred ({}, {})'.format(r.status_code, r.text))
        else:
            if r.status_code == 401:
                print(
                    'An authentication error occurred while connecting to {}. Please check your credentials, then try again.'.format(
                        self.cluster_ip))
                sys.exit()

        if return_json:
            return r.json()
        else:
            return r

    def verify_ssl(self, value=True):
        self.verify = value

    def get_k8s_clusters(self):

        result = self.get_info(cookie=self.cookie)
        k8s_clusters = {}

        for cluster in result:
            k8s_clusters[cluster['cluster_metadata']['name']] = cluster['cluster_metadata']['uuid']

        return k8s_clusters

    def get_kubeconfig(self, k8s_name):

        k8s_list = self.get_k8s_clusters()
        if k8s_name in k8s_list:
            self.method = 'get'
            self.request_url = "{}/{}".format(self.base_url, 'cluster/{}/kubeconfig'.format(k8s_list[k8s_name]))
            result = self.get_info(cookie=self.cookie)
            kubeconfig = base64.b64decode(result['yml_config'])
            return kubeconfig.decode('UTF-8')
        else:
            return None





