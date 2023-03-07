"""
Kinescraper is a package for downloading videos from Kinescope. It downloads video content using the direct link to the Kinescope video. This link must lead directly to the video without any extra content, it can be found using dev tools on the original webpage and it starts with "https://kinescope.io/..."

requirements:
requests                2.28.2
undetected-chromedriver 3.4.6
"""

__version__ = '1.0'

from .undet_chrome import UnDetChrome
from .kinescraper import scrape, download, merge_files

__all__ = ['UnDetChrome', 'scrape', 'download', 'merge_files']

