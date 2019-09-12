import ipwhois
from pprint import pprint
from pathlib import Path
import json
import queue
import logging
from threading import Thread


def multithread_approach():
    q = queue.Queue()

    input_file = Path.cwd() / 'resources' / 'results.txt'

    with open(input_file, 'r') as f:
        ips = f.read().split('\n')

    for ip in ips:
        q.put(ip)

    def lookup(q, entitie):
        while not q.empty():
            ip_in = q.get()
            try:
                ip_info = ipwhois.IPWhois(ip_in).lookup_rdap()

                if 'asn_description' in ip_info:
                    entitie[ip_info.get('asn_description')] = ip_info
                else:
                    entitie[ip_in] = ip_info
            except Exception as e:
                logging.debug(f'Unable to lookup IP {ip} because of error: {e}')

            q.task_done()
        return True

    entities = dict()

    for i in range(10):
        logging.debug(f'Starting thread {i}')
        worker = Thread(target=lookup, args=(q, entities))
        worker.setDaemon(True)
        worker.start()

    q.join()

    logging.info('all ips completed')

    output_file = Path.cwd() / 'resources' / 'output.json'

    with open(output_file, 'w') as f:
        json.dump(entities, f)


# def lookup_ips():
#     for i, ip in enumerate(ips[0:6000]):
#         try:
#             ip_info = ipwhois.IPWhois(ip).lookup_rdap()
#
#             if 'asn_description' in ip_info:
#                 entities[ip_info.get('asn_description')] = ip_info
#             else:
#                 entities[ip] = ip_info
#
#         except Exception as e:
#             print(f'Unable to lookup IP {ip} because of error: {e}')
#
#         print(f'finished ip {i}/6000')
#
#     output_file = Path.cwd() / 'resources' / 'output.json'
#
#     with open(output_file, 'w') as f:
#         json.dump(entities, f)


def main():
    # lookup_ips()
    multithread_approach()

if __name__ == '__main__':
    main()
    # pprint(ipwhois.IPWhois('104.24.122.53').lookup_rdap())
