import atexit

import requests
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Scraper:
    def __init__(self):
        self.html = ''
        self.headers = Headers(browser='firefox', os='lin').generate()
        self.driver = None
        self.session = None
        self.driver_path = ''

        atexit.register(self.terminate)

    def requests_get(self, url):
        response = requests.get(url, headers=self.headers)
        self.html = response.text

    def __driver_init(self):
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            desired_capabilities=caps,
        )

    def get(self, url):
        if not self.driver:
            self.__driver_init()
        self.driver.get(url)

    def parse(self):
        html = str(self.driver.page_source)
        return html

    def terminate(self):
        if self.driver:
            self.driver.quit()

    def refresh(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.CONTROL + 'r')
