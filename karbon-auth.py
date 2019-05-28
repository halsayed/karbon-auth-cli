#!/usr/bin/env python3

from lib.karbon import KarbonClient
from lib.karbon import PrismAuthenticate
import argparse
import getpass


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('pc_host', help='Host name or ip address of Prism Central')
    parser.add_argument('k8s_name', help='Name of the kubernetes cluster deployed by Karbon')
    parser.add_argument('-u', '--username', help='Username to authenticate with Prism Central')
    parser.add_argument('-p', '--password', help='Password to authenticate with Prism Central')

    args = parser.parse_args()

    cluster_ip = args.pc_host
    karbon_cluster = args.k8s_name

    if args.username:
        username = args.username
    else:
        username = input('Username: ')

    if args.password:
        password = args.password
    else:
        password = getpass.getpass('Password: ')

    prism_auth = PrismAuthenticate(cluster_ip, username, password)
    prism_auth.verify_ssl(False)
    cookie = prism_auth.get_cookie()

    karbon = KarbonClient(cluster_ip, cookie)
    karbon.verify_ssl(False)
    kuebconfig = karbon.get_kubeconfig(karbon_cluster)

    if kuebconfig:
        print(kuebconfig)
        exit(0)
    else:
        print('Karbon cluster {} not found ...'.format(karbon_cluster))
        exit(1)


if __name__ == '__main__':
    main()


