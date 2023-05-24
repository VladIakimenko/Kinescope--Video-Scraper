import os
import atexit

import requests
import undetected_chromedriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class UnDetChrome:
    def __init__(self):
        """
    --headless: Runs the browser in headless mode, which means that the browser window will not be displayed while it runs in the background. This can be useful for running automated tests and web scraping tasks, but it is important to also consider implementing additional measures to avoid detection and ensure successful completion of tasks.
    --disable-blink-features=AutomationControlled: Disables Blink features that are controlled by Automation. This option is commonly used to bypass browser detection techniques used by websites to prevent web scraping.
    --disable-extensions: Disables all extensions from being loaded in the browser. This can improve browser performance and prevent extensions from interfering with the web scraping process.
    --disable-gpu: Disables the use of the GPU in the browser. This can improve browser stability and performance.
    --disable-features=IsolateOrigins,site-per-process: Disables certain browser features that can potentially interfere with web scraping. IsolateOrigins isolates web page origins from each other, while site-per-process runs each site in its own process. Disabling these features can help avoid issues with cookies and sessions.
    --enable-javascript: Enables JavaScript in the browser. This is often necessary for web scraping, as many websites rely on JavaScript to load and display content.
    --no-sandbox: Disables the sandbox mode of the browser. This can improve browser performance and prevent issues related to running the browser in a sandbox.
    --start-maximized: Starts the browser in maximized mode. This can help ensure that the content being scraped is visible and accessible.
    --ignore-certificate-errors: Ignores certificate errors in the browser. This can help prevent issues related to HTTPS certificates, which may be encountered when scraping HTTPS websites.
    --disable-dev-shm-usage: Disables the use of the /dev/shm partition in the browser. This can help prevent issues related to the partition being full or unavailable.
    --disable-popup-blocking: Disables the browser's pop-up blocker. This can be useful when scraping websites that rely on pop-ups to display content or navigate.
        """
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        options = undetected_chromedriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        options.add_argument("--enable-javascript")
        options.add_argument("--no-sandbox")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-popup-blocking")
        
#       options.binary_location = '/usr/bin/google-chrome-stable'

        self.driver = undetected_chromedriver.Chrome(desired_capabilities=caps, options=options)
        self.driver.start_client()
        atexit.register(self.terminate)

    def get(self, url):
        self.driver.get(url)

    def parse(self):
        html = str(self.driver.page_source)
        return html

    def terminate(self):
        self.driver.close()
        self.driver.quit()
        print('Undetected ChromeDriver closed.')
