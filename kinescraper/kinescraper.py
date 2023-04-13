import datetime
import subprocess
import threading
import time
import os
import json
import curses

import requests
from selenium.webdriver.common.keys import Keys

from .file_joiner import join_files

FFMPEG_CMD = 'kinescraper/merge.txt'


def scrape(scraper, duration, step):
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    curses.halfdelay(1 * 10)

    scraper.driver.switch_to.active_element.send_keys(Keys.SPACE)
    start_time = datetime.datetime.now()
    result = []

    def wind_forward(scraper, flag):
        while not flag.is_set():
            time.sleep(5)
            for _ in range(step):
                scraper.driver.switch_to.active_element.send_keys(Keys.ARROW_RIGHT)

    def detect_requests(scraper, flag, result):
        print(f'Detecting requests from kinescope... ({duration} seconds)\n'
              f'Press "q" to terminate manually\n')
        def process_browser_log_entry(entry):
            response = json.loads(entry['message'])['message']
            return response

        while not flag.is_set():
            browser_log = scraper.driver.get_log('performance')
            events = [process_browser_log_entry(entry) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            if events:
                if events[-1]['params'].get('response'):
                    link = events[-1]['params']['response']['url']
                    if 'videos' in link and link not in result:
                        result.append(link)
        return result

    timer_flag = threading.Event()
    detector_flag = threading.Event()

    timer = threading.Thread(target=wind_forward, args=(scraper, timer_flag))
    timer.start()

    detector = threading.Thread(target=detect_requests, args=(scraper, detector_flag, result))
    detector.start()
    
    print()
    stdscr.addstr(f'Press any key if finished earlier!\n')
    while (datetime.datetime.now() - start_time).total_seconds() < duration:
        remaining_time = round(duration - (datetime.datetime.now() - start_time).total_seconds())
        if remaining_time > 0:
            # print(f'\r{remaining_time} seconds remain   ', end='')
            stdscr.addstr(f'\r{remaining_time} seconds remain   ')

        c = stdscr.getch()
        if c != curses.ERR:
            timer_flag.set()
            detector_flag.set()
            break
    else:
        print("\rTime's up!" + ' ' * 30)
        timer_flag.set()
        detector_flag.set()

    scraper.driver.minimize_window()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    return result


def download(urls, links_log='links_log'):
    print(f'\n{len(urls)} unique requests detected.')
    
    with open(links_log, 'wt') as f:
        for url in urls:
            f.write(url + '\n')

    files = []
    audio_counter = 0
    video_counter = 0
    resolutions = {}

    for url in urls:
        if 'audio' not in url:
            res = url.partition('?')[0].rpartition('/')[-1].rstrip('mp4')
            resolutions[res] = resolutions.get(res, 0) + 1
    print(f'Following chunks resolutions detected: {resolutions}')
    target_resolution = max(resolutions, key=lambda x: resolutions.get(x))
    print(f'Target resolution: {target_resolution}')

    for url in urls:
        if 'audio' not in url and target_resolution not in url:
            continue
        file_type = ('video', 'audio')['audio' in url]
        i = (video_counter, audio_counter)[file_type == 'audio']
        print(f'\nReceiving content from {url}')
        response = requests.get(url)
        print('Creating file...')
        file = f'{file_type}_{i}.mp4'
        with open(file, 'wb') as f:
            f.write(response.content)
        print(f'File {file} created')
        files.append(file)
        if file_type == 'audio':
            audio_counter += 1
        else:
            video_counter += 1

    print('\nDownloading accomplished.')
    return files


def merge_files(input_files, output_file='output.mp4', ffmpeg_log='ffmpeg_log.txt'):
    audio_files = sorted([file for file in input_files if 'audio' in file])
    print(f'\nTemporary audio files downloaded: {", ".join(audio_files)}')
    
    video_files = sorted([file for file in input_files if 'video' in file])
    print(f'Temporary video files downloaded: {", ".join(video_files)}')

    print('Putting the whole thing together...')

    if not len(audio_files) and len(video_files):
        print('\nNo valid content collected!')
    else:
        join_files(audio_files, 'audio.mp4')
        join_files(video_files, 'video.mp4')

        if os.path.exists('audio.mp4') and os.path.exists('video.mp4'):
            if os.path.exists(output_file):
                os.remove(output_file)
            with open(ffmpeg_log, 'wt', encoding='UTF-8') as log:
                with open (FFMPEG_CMD, 'rt', encoding='UTF-8') as f:
                    ffmpeg_cmd = f.read()
                subprocess.call(ffmpeg_cmd, shell=True, stderr=log)
            if os.path.exists(output_file):
                print(f'\n{output_file} has been created! Good job, Gansta!')
        else:
            print('\nCan not merge files!')

    while True:
        reply = input('Kill temps? ("y" or "n")\t').lower().strip()
        if reply == 'y':
            for file in (input_files + ['audio.mp4', 'video.mp4']):
                if os.path.exists(file):
                    os.remove(file)
            print('\nTemporary files removed.')
            break
        if reply == 'n':
            break
            

