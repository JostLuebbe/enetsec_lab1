import ipwhois
from pprint import pprint
from pathlib import Path
import json


def main():
    input_file = Path.cwd() / 'resources' / 'results.txt'

    with open(input_file) as f:
        ips = f.read().split('\n')

    entities = dict()

    for i, ip in enumerate(ips):
        ip_info = ipwhois.IPWhois(ip).lookup_whois()
        if ip_info.get('nets'):
            first_net = ip_info.get('nets')[0]

            if not first_net.get('name') in entities:
                entities[first_net.get('name')] = {
                    'found_ips': [],
                    'subnets': set()
                }

            e = entities.get(first_net.get('name'))
            e['found_ips'].append(ip)

            for net in ip_info.get('nets'):
                e['subnets'].add(net.get('cidr'))
        else:
            print(f'could not find whois info for {ip}')
        print(f'finished lookup for ip {i}/{len(ips)}')

    output_file = Path.cwd() / 'resources' / 'output.json'

    with open(output_file) as f:
        json.dump(entities, f)


    # pprint(entities)


if __name__ == '__main__':
    main()