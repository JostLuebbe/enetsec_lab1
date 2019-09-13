import ipwhois
from pprint import pprint
from pathlib import Path
import json
import queue
import logging
from threading import Thread
import time
from time import sleep

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.ERROR)


def multithread_approach():
    q = queue.Queue()
    logger.debug(f'Created queue {q}')

    input_file = Path.cwd() / 'resources' / 'results.txt'

    with open(input_file, 'r') as f:
        ips = f.read().split('\n')

    logger.debug(f'read in list of ips of length {len(ips)}')

    for ip in ips:
        q.put(ip)

    def lookup(q, e):
        while not q.empty():
            # sleep(1)
            ip_in = q.get()
            try:
                ip_info = ipwhois.IPWhois(ip_in).lookup_rdap()

                if 'asn_description' in ip_info:
                    e[ip_info.get('asn_description')] = ip_info
                else:
                    e[ip_in] = ip_info
            except Exception as exception:

                if 'Rate' in exception:
                    sleep(10)
                logger.error(f'Unable to lookup IP {ip} because of error: {exception}')

            logger.debug(f'finished ip {ip_in}')
            q.task_done()
        return True

    entities = dict()

    for i in range(10):
        logger.debug(f'Starting thread {i}')
        worker = Thread(target=lookup, args=(q, entities))
        worker.setDaemon(True)
        worker.start()
        logger.debug(f'started thread {i}')

    q.join()

    logger.debug('all ips completed')

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


def main():
    # start_time = time.time()
    # lookup_ips()
    # print(time.time() - start_time)
    start_time = time.time()
    multithread_approach()
    print(time.time() - start_time)

if __name__ == '__main__':
    main()
    # pprint(ipwhois.IPWhois('104.24.122.53').lookup_rdap())
