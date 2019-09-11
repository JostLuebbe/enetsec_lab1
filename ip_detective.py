import ipwhois
from pprint import pprint
from pathlib import Path
import json
from urllib.error import HTTPError
import socket


def lookup_ips():
    input_file = Path.cwd() / 'resources' / 'results.txt'

    with open(input_file, 'r') as f:
        ips = f.read().split('\n')

    entities = dict()

    for i, ip in enumerate(ips[0:6000]):
        try:
            ip_info = ipwhois.IPWhois(ip).lookup_rdap()

            if 'asn_description' in ip_info:
                entities[ip_info.get('asn_description')] = ip_info
            else:
                entities[ip] = ip_info

        except Exception as e:
            print(f'Unable to lookup IP {ip} because of error: {e}')

        print(f'finished ip {i}/6000')

    output_file = Path.cwd() / 'resources' / 'output.json'

    with open(output_file, 'w') as f:
        json.dump(entities, f)


def main():
    lookup_ips()


if __name__ == '__main__':
    main()