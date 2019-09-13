from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pathlib import Path
import scapy.all

from tbselenium.tbdriver import TorBrowserDriver


site_urls = [
    'https://en.wikipedia.org/wiki/Cat',
    'https://en.wikipedia.org/wiki/Dog',
    'https://en.wikipedia.org/wiki/Egress_filtering',
    'http://web.mit.edu/',
    'http://www.unm.edu/',
    'https://www.cmu.edu/',
    'https://www.berkeley.edu/',
    'https://www.utexas.edu/',
    'https://www.asu.edu/',
    'https://www.utdallas.edu/'
]


def regular_browser():
    geckodriver_path = Path('/home/class/Downloads/geckodriver')

    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=geckodriver_path)

    for url in site_urls:
        driver.get(url)


def tor_browser():
    binary_path = '/home/class/Downloads/tor-browser_en-US/Browser/firefox'

    firefox_binary = FirefoxBinary(binary_path)
    driver = webdriver.Firefox(firefox_binary=firefox_binary)

    for url in site_urls:
        driver.get(url)

    # with TorBrowserDriver('/home/class/Downloads/tor-browser_en-US', tbb_logfile_path='./tor_logs/') as driver:
    #     print(driver.load_url('https://www.asu.edu/'))
        # for url in site_urls:
        #     driver.get(url)


def main():
    t = AsyncSniffer()
    t.start()
    regular_browser()
    # tor_browser()
    t.stop()
    wrpcap('scapytest.pcap', t.results)


if __name__ == '__main__':
    main()
