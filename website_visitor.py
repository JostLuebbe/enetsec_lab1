from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pathlib import Path

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
    with TorBrowserDriver('/home/class/Downloads/tor-browser_en-US') as driver:
        print(driver.load_url('https://www.asu.edu/'))
	# for url in site_urls:
        #    driver.get(url)


def main():
    # regular_browser()
    tor_browser()


if __name__ == '__main__':
    main()
