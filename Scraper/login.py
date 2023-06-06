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
options.headless = False
chro_path = os.environ.get('CHROME_PATH')
driver = webdriver.Chrome(options=options)

driver.get("https://www.twitter.com/login")
print(driver.current_url)

print("Opening twitter account...")

basedir = os.path.dirname(os.path.abspath(__file__))
account_info = os.path.join(basedir, '../Authentication/Account.txt')
#log in into an account
def login():
    f=open(account_info)

    lines=f.readlines()
    username=lines[0]
    password=lines[1]
    phoneNo=lines[2]
    time.sleep(5)
    try:
        try:
            wait = WebDriverWait(driver, 5)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
            element.send_keys(username)
            time.sleep(3)
        except:
            wait = WebDriverWait(driver, 5)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
            element.send_keys(username)
            time.sleep(3)
        try:
            wait = WebDriverWait(driver, 5)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
            element.send_keys(password)
            time.sleep(3)
            if driver.get(url='https://twitter.com/home'):
                pass
            else:
                try:
                    wait = WebDriverWait(driver, 5)
                    element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
                    element.send_keys(phoneNo)
                    f.close()
                    time.sleep(3)
                except:
                    pass
        except:
            pass
        if driver.get(url='https://twitter.com/home'):
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
                element.send_keys(phoneNo)
                time.sleep(3)

                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
                element.send_keys(password)
                time.sleep(3)
            except:
                wait = WebDriverWait(driver, 5)
                element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
                element.send_keys(password)
                time.sleep(3)
        else:
            pass

    except:
        driver.refresh()
        driver.get("https://www.twitter.com/login")
        login()

