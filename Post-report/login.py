from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os


from selenium.webdriver.common.keys import Keys

import time
#from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
# Assigning a link to a webdriver

chromedriver_autoinstaller.install()
options = Options()
options.headless = True
chro_path = os.environ.get('CHROME_PATH')
driver = webdriver.Chrome(options=options)

driver.get("https://www.twitter.com/login")
print(driver.current_url)

print("Opening twitter account...")

#log in into an account
def login():
    f=open("/home/ubuntu/Documents/twitterProject/Authentication/Account.txt")

    lines=f.readlines()
    username=lines[0]
    password=lines[1]
    phoneNo=lines[2]
    time.sleep(5)
    try:
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
    except:
        driver.refresh()
        driver.get("https://www.twitter.com/login")
        login()