import os
import sys
import time
import json

import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import *
from kinescraper import *


def read_pass():
    if os.path.exists(PASS_PATH):
        with open(PASS_PATH, 'rt', encoding='UTF-8') as file:
            password = file.read().rstrip()
    else:
        directory = PASS_PATH.replace('\\', '/').rpartition('/')[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(PASS_PATH, 'wt', encoding='UTF-8') as file:
            password = input('Enter password: ')
            file.write(password)
    return password


def create_paths():
    for line in (OUTPUT, LINKS_LOG, FFMPEG_LOG):
        path = line.replace('\\', '/').rpartition('/')[0]
        if path and not os.path.exists(path):
            os.makedirs(path)


def authorize(scraper, password):
    print('\nClicking the "accept cookies" button...')
    submit_button = WebDriverWait(scraper.driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']")))
    submit_button.click()
    print('Clicked.')

    print('\nClicking the "authorize" button...')
    button = WebDriverWait(scraper.driver, 20).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'a.src-LMS-components'
                          '-Errors-components-No'
                          'Access--goback--dxBzz'
                          '.blue_button')))
    button.click()
    print('Clicked.')

    print('\nEntering e-mail...')
    email_input = WebDriverWait(scraper.driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, '//input[@name="email"]')))
    email_input.send_keys(EMAIL)
    print('Done.')

    print('\nEntering password...')
    pass_input = scraper.driver.find_element(By.XPATH, '//input[@class="node_modules-'
                                                        '@netology-shared-src-r'
                                                        'eallyShared-authorization-moda'
                                                        'ls-SignIn--input--LsO8Q"]')
    pass_input.send_keys(password)
    print('Done.')

    print('\nClicking the "submit" button...')
    submit_button = WebDriverWait(scraper.driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']")))
    submit_button.click()
    print('Clicked.')

    print('\nSubtracting video to a separate window...')
    element = WebDriverWait(scraper.driver, 40).until(EC.element_to_be_clickable(
        (By.XPATH, "//iframe[contains(@id, 'kinescope_video_player')]")))
    time.sleep(3)
    link = element.get_attribute('src')
    scraper.get(link)
    print('Done.')

#    print('\nStarting video playback...')
#    time.sleep(5)
#    iframe = scraper.driver.find_element(By.XPATH,
#                                          '//iframe')
#    scraper.driver.switch_to.frame(iframe)
#    scraper.driver.switch_to.active_element.send_keys(Keys.SPACE)
#    time.sleep(3)
#    print('Playing.')

    print()


if __name__ == '__main__':
    pass_ = read_pass()
    create_paths()

    parser = UnDetChrome()
    parser.get(URL)
    authorize(parser, pass_)

    print('.' * 50)
    links = scrape(parser, duration=DURATION, step=STEP)

    print('.' * 50)
    file_list = download(links, links_log=LINKS_LOG)

    print('.' * 50)
    merge_files(sorted(file_list), output_file=OUTPUT, ffmpeg_log=FFMPEG_LOG)
