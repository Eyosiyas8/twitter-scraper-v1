import json
import twint
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import os
import pandas as pd
import time
from sys import platform
# from colored import stylize
# import colored 
from log import *
import re
from login import *
import csv
from lxml import etree
import configparser
import requests
from bs4 import BeautifulSoup
def acc_info(dom):
    image_link = []
    # dom.xpath('//div[@class="css-1dbjc4n r-1awozwy r-1hwvwag r-18kxxzh r-1b7u577"]')[0].click
    time.sleep(1)
    fullname = dom.xpath('.//span[@class="css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0"]/span')[0].text
    print(fullname)
    username = dom.xpath('.//div[@class="css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]/span')[0].text
    print(username)
    time.sleep(0.2)
    try:
        description = dom.xpath('.//div[@class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-1h8ys4a r-1jeg54m r-qvutc0"]/span')[0].text
        print(description)
    except:
        description = ''
    profile_image = ''
    try:
        image_links = dom.xpath('.//div[@class="css-1dbjc4n r-1adg3ll r-1udh08x"]//img')
        for i in range(len(image_links)):  
            profile_image = image_links[0].attrib['src'] 
            image = image_links[i].attrib['src'] 
            if i==0 or 'profile_images' in image:
                continue             
            image_link.append(image)
        print(image_link)
    except:
        print(None)
        pass
        # tweets.append(tweet_text)
    account_info = (fullname, username, description, profile_image)
    return account_info
          
