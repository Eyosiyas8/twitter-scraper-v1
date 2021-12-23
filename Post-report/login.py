from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
#from bs4 import BeautifulSoup

from selenium.common.exceptions import NoSuchElementException
# Assigning a link to a webdriver

driver = webdriver.Chrome(executable_path=r"/home/osint/Desktop/OSINT/Twitter/twitterScraper/chromedriver/chromedriver")
driver.get("https://www.twitter.com/login")
print(driver.current_url)

print("Opening twitter account...")

#log in into an account
def login():
    f=open("/home/osint/Desktop/OSINT/Twitter/twitterScraper/Authentication/account.txt")

    lines=f.readlines()
    username=lines[0]
    password=lines[1]
    phoneNo=lines[2]
    time.sleep(5)
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        element.send_keys(username)
        time.sleep(1)
    except:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        element.send_keys(username)
        time.sleep(1)
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        element.send_keys(password)
        time.sleep(1)
    except:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        element.send_keys(phoneNo)
        time.sleep(1)

    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        element.send_keys(password)
        f.close()
        time.sleep(1)
    except:
        NoSuchElementException