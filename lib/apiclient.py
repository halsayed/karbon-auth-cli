
import sys
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class ApiClient():

    def __init__(self, method, cluster_ip, request, body, username, password, version='',
                 root_path='api/nutanix', port='9440', verify=True):
        self.method = method
        self.cluster_ip = cluster_ip
        self.username = username
        self.password = password
        self.verify = verify
        if version == '':
            self.base_url = "https://{}:{}/{}".format(self.cluster_ip, port, root_path)
        else:
            self.base_url = "https://{}:{}/{}/{}".format(self.cluster_ip, port, root_path,version)
        self.entity_type = request
        self.request_url = "{}/{}".format(self.base_url, request)
        self.body = body

    def get_info(self, show_info=False, return_json=True, cookie=''):

        if show_info == True:
            print("Requesting '{}' ...".format(self.entity_type))

        if not self.verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        if cookie == '':
            headers = {'Content-Type': 'application/json; charset=utf-8'}
        else:
            headers = {'Content-Type': 'application/json; charset=utf-8', 'Cookie': cookie}
        try:
            if(self.method == 'post'):
                r = requests.post(self.request_url, data=self.body, verify=self.verify, headers=headers, auth=HTTPBasicAuth(self.username, self.password), timeout=60)
            else:
                r = requests.get(self.request_url, verify=self.verify, headers=headers, auth=HTTPBasicAuth(self.username, self.password), timeout=60)
        except requests.ConnectTimeout:
            print('Connection timed out while connecting to {}. Please check your connection, then try again.'.format(self.cluster_ip))
            sys.exit()
        except requests.ConnectionError:
            print('An error occurred while connecting to {}. Please check your connection, then try again.'.format(self.cluster_ip))
            sys.exit()
        except requests.HTTPError:
            print('An HTTP error occurred while connecting to {}. Please check your connection, then try again.'.format(cluster_ip))
            sys.exit()

        if r.status_code >= 500:
            print('An HTTP server error has occurred ({}, {})'.format(r.status_code, r.text))
        else:
            if r.status_code == 401:
                print('An authentication error occurred while connecting to {}. Please check your credentials, then try again.'.format(self.cluster_ip))
                sys.exit()
            #if r.status_code > 401:
                #print(json.loads(r.text)['message_list'][0]['message'])
                #sys.exit()
            # else:
                # print('Connected and authenticated successfully.')

        if return_json:
            return r.json()
        else:
            return r
