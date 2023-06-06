# num = 10
# num2 = 11


# def sum(num1, num3):
#     total = num1+num3
#     print(total)

# sum(num, num2)

# my_list = [1, 2, 3]
# my_iterator = iter(my_list)

# for lists in my_list:
#     print(lists)
#     print(next(my_iterator))
#     print('list', lists)



from selenium import webdriver
from bs4 import BeautifulSoup
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


chromedriver_autoinstaller.install()
options = Options()
options.headless = False
chro_path = os.environ.get('CHROME_PATH')
driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome(options=options)
driver.get("http://www.example.com")

soup = BeautifulSoup(driver.page_source, 'html.parser')
parent_tag = soup.find('div', {'id': 'parent'})

wait = WebDriverWait(driver, 1)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='{}']".format(parent_tag['id']))))
element = element.text
wait = WebDriverWait(driver, 1)
element = wait.until(EC.presence_of_element_located((By.XPATH, "./*")))
