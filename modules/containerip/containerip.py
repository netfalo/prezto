#!/usr/bin/python

import sys
import argparse
from docker import Client


def list_ips(client, container_name, quiet):
    container = client.inspect_container(container_name)
    networks = container['NetworkSettings']['Networks']
    for network in networks:
        if quiet:
            print(networks[network]['IPAddress'])
            return
        else:
            print(network + ': ' + networks[network]['IPAddress'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get ip of container.')
    parser.add_argument('-q', help=' just print the first available ip.', action='store_true')
    parser.add_argument('container_name', help='name of the container.')
    args = parser.parse_args()

    client = Client()
    name = args.container_name
    exists = False
    running = False
    for container in client.containers(all=True, filters={'name' : name}):
        if '/' + name in container['Names']:
            exists = True
            running = container['State'] == 'running'
    if not exists:
        print('Not existing container')
        sys.exit()
    if not running:
        print('Not running container')
        sys.exit()
    list_ips(client, name, args.q)
