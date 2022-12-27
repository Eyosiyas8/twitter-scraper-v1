from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import os
import sys
#import welcome
dependancies = os.environ.get('DEPENDANCIES')
print(dependancies)
sys.path.insert(1, dependancies)
import colored
import time
from colored import stylize
import pandas as pd
import time
from sys import platform
import configparser
from log import *
# from colored import stylize
import twint


basedir = os.path.dirname(os.path.abspath(__file__))
print(basedir)

config = configparser.ConfigParser()
elements_file = os.path.join(basedir, '../Authentication/elements_iteration.ini')
config.read(elements_file)
web_elements = config['WebElements']
iteration_number = config['IterationNumber']
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

# Profile information scraper
def profile_scraper(username, csv_profile):
    '''
    :param username: This is the username from which the profile information is scraped from
    :param csv_file: This is the pre-initialized file that the user profile information is saved.
    
    This function takes username and csv_file as an argument and returns the profile information of a user in csv file format.
    '''
    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('Fullname'))))
        Fullname = element.text
        print("Fullname: " + Fullname)
    except:
        Fullname = None
        print(None)

    try:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('Description'))))
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
    
    # Save the data on csv_profile
    df.to_csv(csv_profile)

# Scrapes tweets that contain a given keyword using twint
def scraper(Keyword, csv_keyword, since, until):
    '''
    :param Keyword: The keyword provided by the user that the scraper uses.
    :param csv_keyword: The file in which all scraped tweets by the given keyword are saved.
    :param since: The starting date for scraping.
    :param until: The last date for scraping.

    This function takes the keyword, since, until and the csv_keyword arguments and feed them to twints config format to scrape tweets that contain a given keyword within the provided timeframe before saving it to csv_keyword file.
    '''
    # Configure
    c = twint.Config()
    #c.Username = username
    c.Store_csv = True
    c.Since = since
    c.Resume = 'tweet.raw'
    c.Until = until
    c.Output = csv_keyword
    c.Count = True
    c.Search = Keyword
    c.Limit = 100
    # c.Verified = True 

    # Run
    # Set iteration number to scrape more data
    # Log total numbre of scraped tweets in log/INFO.log
    if csv_keyword:
        try:
            for i in range(int(iteration_number.get('Keyword_tweet'))):
                total_count = 0
                
                time.sleep(3)
                twint.run.Search(c)
            #     total_count += int(c.Count)
            # message = 'Number of scraped tweets is ' + str(total_count)
            # info_log(message)
            os.remove('tweet.raw')

        # Error handler
        # Log error in log/ERROR.log
        except Exception as e:
            message = str(e)+' Scraping for ' + Keyword + ' keyword has failed '
            error_log(message)
            for i in range(3):
                twint.run.Search(c)
            try:
                os.remove('tweet.raw')
            except Exception as e:
                print('No such file! ' + e)

        # stylize('Scraping for ' + Keyword + ' keyword has failed ', colored.fg("red"))
        # stylize(e, colored.fg("grey_46"))
        #print(colored(100, e))
    else:
        scraper(Keyword, csv_keyword, since, until)

# Scrape replies
def scrape_replies(username, csv_raw_reply):
    n = twint.Config()
    n.Search = "@" + username
    n.Replies = True
    n.Since = "2022-08-04"
    #n.Until = until
    n.To = username
    n.Count = True
    n.Resume = 'reply.raw'
    n.Store_csv = True
    n.Output = csv_raw_reply

    # Run
    # Set iteration number to scrape more data
    # Log total numbre of scraped tweets in log/INFO.log
    try:
        for i in range(int(iteration_number.get('Keyword_reply'))):
            total_count = 0
            time.sleep(1)
            twint.run.Search(n)
            # total_count += int(c.Count)
        # message = 'Number of scraped replies is ' + str(total_count)
        # info_log(message)
        os.remove('reply.raw')

    # Error handler
    # Log error in log/ERROR.log
    except Exception as e:
        message = str(e)+' \nScraping for replies to ' + Keyword + '\'s account has failed '
        error_log(message)
        print('Scraping for replies to ' + Keyword + ' has failed')
        # print(colored(255, 100, 100, e))


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
time.sleep(0.5)
