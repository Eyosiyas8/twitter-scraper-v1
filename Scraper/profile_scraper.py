from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import os
import pandas as pd
import time
from sys import platform
basedir = os.path.dirname(os.path.abspath(__file__))

"""
if platform == "linux" or platform == "linux2":
    chro_path = os.path.join(basedir, '../chromedriver/chromedriver')
elif platform == "win32":
    chro_path = os.path.join(basedir, '../chromedriver/chromedriver.exe')
    
"""
chromedriver_autoinstaller.install()
options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)

data_set = []
# print(search_page)
# open("twitterpage.text","w").write(search_page.encode('utf-8'))

# Profile scraper
def profile_scraper(username, csv_file):
    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-adyw6z r-1vr29t4 r-135wba7 r-bcqeeo r-1udh08x r-qvutc0"]/span[1]/span')))
        Fullname = element.text
        print("Fullname: " + Fullname)
    except:
        Fullname = None
        print(None)

    try:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/span')))
        Description = element.text
        print("Description: " + Description)
    except:
        Description = None
        print(None)
    try:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div/div')))
        Tweets = element.text
        print("Number of tweets: "+Tweets)
    except:
        Tweets = None
        print(None)

    try:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]/div[1]/a//span')))
        No_Following = element.text
        print(No_Following)
    except:
        No_Following = None
        print(None)

    try:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]/div[2]/a//span')))
        No_Followers = element.text
        print(No_Followers)

    except:
        No_Followers = None
        print(None)

    try:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "@")]')))
        UserName = element.text
        print("Username: "+UserName)
    except:
        UserName = None
        print(None)

    try:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "Joined")]')))
        Joined_date = element.text
        print(Joined_date)
    except:
        Joined_date = None
        print(Joined_date)

    df = pd.DataFrame(
        [[Fullname, UserName, Description, Tweets, No_Following, No_Followers, Joined_date]],
        columns=['Fullname', 'UserName', 'Description', 'Tweets', 'Number of Followings', 'Number of Followers',
                 'Joined_date'])
    
    #file = os.path.join(basedir, '../csv_files/')
    df.to_csv(csv_file)

'''
with open("C:/Users/User/PycharmProjects/twitterScraper/venv/Scripts/Authentication/Document.txt","r", encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    for i in range(len(lines)):
        username=lines[i]
        url = "https://twitter.com/%s" % username
        driver.get(url)
        print(url)
        profile_scraper()

'''
time.sleep(1)
