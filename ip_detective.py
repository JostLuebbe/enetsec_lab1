import ipwhois
from pprint import pprint
from pathlib import Path
import json
import queue
import logging
from threading import Thread
import time
from time import sleep
import netaddr
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def multithread_approach():
    q = queue.Queue()
    logger.debug(f'Created queue {q}')

    input_file = Path.cwd() / 'resources' / 'results2.txt'

    with open(input_file, 'r') as f:
        ips = f.read().split('\n')

    logger.debug(f'read in list of ips of length {len(ips)}')

    for ip in ips[0:6000]:
        q.put(ip)

    def lookup(q, e):
        while not q.empty():
            # sleep(1)
            ip_in = q.get()
            try:
                ip_info = ipwhois.IPWhois(ip_in).lookup_rdap()
                e[ip_in] = ip_info
            except Exception as exception:
                if 'Rate' in str(exception):
                    sleep(10)
                logger.error(f'Unable to lookup IP {ip} because of error: {exception}')

            logger.debug(f'finished ip {ip_in}')
            q.task_done()
        return True

    entities = dict()

    for i in range(10):
        # logger.debug(f'Starting thread {i}')
        worker = Thread(target=lookup, args=(q, entities))
        worker.setDaemon(True)
        worker.start()
        # logger.debug(f'started thread {i}')

    q.join()

    logger.debug(f'found results for {len(entities)} ips')

    output_file = Path.cwd() / 'resources' / 'output.json'

    with open(output_file, 'w') as f:
        json.dump(entities, f, indent=4)


def lookup_ips():
    input_file = Path.cwd() / 'resources' / 'results.txt'

    with open(input_file, 'r') as f:
        ips = f.read().split('\n')

    entities = dict()

    for i, ip in enumerate(ips[0:100]):
        try:
            ip_info = ipwhois.IPWhois(ip).lookup_rdap()

            if 'asn_description' in ip_info:
                entities[ip_info.get('asn_description')] = ip_info
            else:
                entities[ip] = ip_info

        except Exception as e:
            logger.error(f'Unable to lookup IP {ip} because of error: {e}')

        logger.info(f'finished ip {i}/6000')

    output_file = Path.cwd() / 'resources' / 'output.json'

    with open(output_file, 'w') as f:
        json.dump(entities, f)


def analysis():
    # input_file = Path.cwd() / 'resources' / 'output.json'
    #
    # with open(input_file, 'r') as f:
    #     ip_dict = json.load(f)
    #
    # entities = {}
    #
    # for ip, info in ip_dict.items():
    #     found = False
    #     for entity in entities:
    #         if info.get('asn_description') ==  entity:
    #             entities[entity]['ips_found'].append(ip)
    #             entities[entity]['cidrs'].append(info.get('asn_cidr'))
    #             found = True
    #
    #     if not found:
    #         entities[info.get('asn_description')] = {
    #             'cidrs': [info.get('asn_cidr')],
    #             'ips_found': [ip]
    #         }
    #
    # with open('resources/anal_output.json', 'w') as f:
    #     json.dump(entities, f, indent=4)

    # 5493/6000 found results


    # input_file = Path.cwd() / 'resources' / 'anal_output.json'
    #
    # with open(input_file, 'r') as f:
    #     entities = json.load(f)
    #
    # for entity in entities:
    #     entities[entity]['num_ips_found'] = len(entities[entity].get('ips_found'))
    #
    #     num_total_ips = 0
    #
    #     for cidr in entities[entity].get('cidrs'):
    #         num_total_ips += netaddr.IPNetwork(cidr).size
    #
    #     entities[entity]['total_ips_in_network'] = num_total_ips
    #
    # with open('resources/anal_output.json', 'w') as f:
    #     json.dump(entities, f, indent=4)

    # input_file = Path.cwd() / 'resources' / 'anal_output.json'
    #
    # with open(input_file, 'r') as f:
    #     entities = json.load(f)
    #
    # total_ips_found = 0
    # max_ips_found = 0
    # max_network = ''
    # min_ips_found = sys.maxsize
    #
    # for network, info in entities.items():
    #     total_ips_found += info.get('num_ips_found')
    #     if info.get('num_ips_found') > max_ips_found:
    #         max_ips_found = info.get('num_ips_found')
    #         max_network = network
    #     if info.get('num_ips_found') < min_ips_found:
    #         min_ips_found = info.get('num_ips_found')
    #
    # print(f'average # of IPs found per network: {total_ips_found/len(entities)}')
    # print(f'max IPs found for a network: {max_ips_found} ({max_network})')
    # print(f'min IPs found for a network: {min_ips_found}')

    pepsi80_file = Path.cwd() / 'pepsi_80.csv'
    pepsi443_file = Path.cwd() / 'pepsi_443.csv'

    with open(pepsi80_file, 'r') as f:
        pepsi_80 = f.read().split('\n')

    ips_80 = netaddr.IPSet(pepsi_80)

    with open(pepsi443_file, 'r') as f:
        pepsi_443 = f.read().split('\n')

    ips_443 = netaddr.IPSet(pepsi_443)

    print(len(ips_80.intersection(ips_443)))
    # print(len(ips_443.intersection(ips_80)))
    print(len(ips_80.difference(ips_443)))
    print(len(ips_443.difference(ips_80)))
    print(ips_80.size)
    print(ips_443.size)


def main():
    # with open('resources/output.json', 'r') as f:
    #     ip_list = json.load(f)
    #
    # print(len(ip_list))

    # start_time = time.time()
    # lookup_ips()
    # print(time.time() - start_time)
    # start_time = time.time()
    # multithread_approach()
    # print(time.time() - start_time)

    start_time = time.time()
    analysis()
    print(time.time() - start_time)


if __name__ == '__main__':
    main()
    # pprint(ipwhois.IPWhois('104.24.122.53').lookup_rdap())
