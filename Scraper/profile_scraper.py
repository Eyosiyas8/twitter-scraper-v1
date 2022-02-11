from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
import time

options = Options()
options.headless = True
chro_path = os.environ.get('CHROME_PATH')
driver = webdriver.Chrome(options=options, executable_path='/home/ubuntu/Desktop/OSINT/Twitter/twitterScraper/chromedriver/chromedriver')

data_set = []
# print(search_page)
# open("twitterpage.text","w").write(search_page.encode('utf-8'))

# Profile scraper
def profile_scraper(username):
    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/span[1]/span')))
        Fullname = element.text
        print("Fullname: " + Fullname)
    except:
        Fullname = None
        print(None)

    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/span')))
        Description = element.text
        print("Description: " + Description)
    except:
        Description = None
        print(None)
    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[2]/div/div')))
        Tweets = element.text
        print("Number of tweets: "+Tweets)
    except:
        Tweets = None
        print(None)

    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]/div[1]/a//span')))
        No_Following = element.text
        print(No_Following)
    except:
        No_Following = None
        print(None)

    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]/div[2]/a//span')))
        No_Followers = element.text
        print(No_Followers)

    except:
        No_Followers = None
        print(None)

    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "@")]')))
        UserName = element.text
        print("Username: "+UserName)
    except:
        UserName = None
        print(None)

    try:
        wait = WebDriverWait(driver, 5)
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
    
    file = os.environ.get('csvFile')
    df.to_csv('/home/ubuntu/Desktop/OSINT/Twitter/twitterScraper/csv_files/' + username + '.csv')

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
time.sleep(5)
