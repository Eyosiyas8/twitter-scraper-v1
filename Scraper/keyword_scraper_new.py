import json
import twint
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
import os
import pandas as pd
import time
from login import *
from sys import platform
# from colored import stylize
# import colored
from log import *
import re
import csv
from lxml import etree
import configparser
import requests
from bs4 import BeautifulSoup

# basedir = os.path.dirname(os.path.abspath(__file__))


# config = configparser.ConfigParser()
# elements_file = os.path.join(basedir, '../Authentication/elements_iteration.ini')
# config.read(elements_file)
# web_elements = config['WebElements']
# iteration_number = config['IterationNumber']

# """
# if platform == "linux" or platform == "linux2":
#     chro_path = os.path.join(basedir, '../chromedriver/chromedriver')
# elif platform == "win32":
#     chro_path = os.path.join(basedir, '../chromedriver/chromedriver.exe')
    
# """
# chromedriver_autoinstaller.install()
# options = Options()
# options.headless = False

# driver = webdriver.Chrome(options=options)
# data_set = []
# # print(search_page)
# # open("twitterpage.text","w").write(search_page.encode('utf-8'))
# print(web_elements.get('Fullname'))
# # Profile information scraper
# def profile_scraper(username, csv_file):
#     '''
#     :param username: This is the username from which the profile information is scraped from
#     :param csv_file: This is the pre-initialized file that the user profile information is saved.

#     This function takes username and csv_file as an argument and returns the profile information of a user in csv file format.
#     '''
#     try:
#         wait = WebDriverWait(driver, 5)
#         element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('UsernameNotFound'))))
#         UsernameNotFound = element.text
#         print(UsernameNotFound)
#         error_log('username '+ username +' not found!')
#         pass
#     except:    
#         try:
#             wait = WebDriverWait(driver, 5)
#             element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('Fullname'))))
#             Fullname = element.text
#             print("Fullname: " + Fullname)
#         except:
#             Fullname = None
#             print(None)

#         try:
#             wait = WebDriverWait(driver, 1)
#             element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('Description'))))
#             Description = element.text
#             print("Description: " + Description)
#         except:
#             Description = None
#             print(None)
#         try:
#             wait = WebDriverWait(driver, 1)
#             element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('Tweets'))))
#             Tweets = element.text
#             print("Number of tweets: "+Tweets)
#         except:
#             Tweets = None
#             print(None)

#         try:
#             wait = WebDriverWait(driver, 1)
#             element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('No_Following'))))
#             No_Following = element.text
#             print(No_Following)
#         except:
#             No_Following = None
#             print(None)

#         try:
#             wait = WebDriverWait(driver, 1)
#             element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('No_Followers'))))
#             No_Followers = element.text
#             print(No_Followers)

#         except:
#             No_Followers = None
#             print(None)

#         try:
#             wait = WebDriverWait(driver, 1)
#             element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('Username'))))
#             UserName = element.text
#             print("Username: "+UserName)
#         except:
#             UserName = None
#             print(None)

#         try:
#             wait = WebDriverWait(driver, 1)
#             element = wait.until(EC.presence_of_element_located((By.XPATH, web_elements.get('Joined_date'))))
#             Joined_date = element.text
#             print(Joined_date)
#         except:
#             Joined_date = None
#             print(Joined_date)
#             pass

#         df = pd.DataFrame(
#         [[Fullname, UserName, Description, Tweets, No_Following, No_Followers, Joined_date]],
#         columns=['Fullname', 'UserName', 'Description', 'Tweets', 'Number of Followings', 'Number of Followers',
#                  'Joined_date'])
    
#     #file = os.path.join(basedir, '../csv_files/')

#     # Save the data on csv_profile
#         df.to_csv(csv_file)

         
            

def keyword_scraper(keyword, dom):
    image_link = []
    try:
        fullname = dom.xpath('.//span[@class="css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0"]/span')[0].text
        print(fullname)
        username = dom.xpath('.//div[@class="css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]/span')[0].text
        print(username)
        time.sleep(0.2)
        try:
            tweet_link = dom.xpath('.//div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]/a')[0].attrib['href']
            tweet_link = 'https://www.twitter.com'+tweet_link
            tweet_id = tweet_link.split("/")[-1]
            print(tweet_id)
            print(type(tweet_id))
            print(tweet_link)
        except:
            tweet_link = ''
            tweet_id = ''
            print("Sponsored Content")
        try:
            if driver.current_url=="https://twitter.com/%s" % main_username:
                print('tweet_url '+driver.current_url)
                conversation_id = tweet_id
                print(conversation_id)
                print(type(conversation_id))
            else:
                print('reply_url '+driver.current_url)
                conversation_id = driver.current_url.split("/")[-1]
                print(conversation_id)
                print(type(conversation_id))
        except Exception as e:
            conversation_id = None
        try:
            post_date = dom.xpath('.//time')[0].attrib['datetime']
            print(post_date)
        except:
            NoSuchElementException
            post_date = ''
        # tweets = dom.xpath('.//div[@data-testid="tweetText"]')
        # tweet_text=''
        # for i in tweets:
        #     comment = dom.xpath(tweets+'/span'+'[i]')
        #     tweet_text+=comment
        tweet_text=''
        full_text = dom.xpath('.//div[@data-testid="tweetText"]')
        all_text = dom.xpath('.//div[@data-testid="tweetText"]/span')
        hashtag = dom.xpath('.//div[@data-testid="tweetText"]/span/a')
        external_link = dom.xpath('.//div[@data-testid="tweetText"]/a')
        mention = dom.xpath('.//div[@data-testid="tweetText"]/div/span/a')
        mentions = []
        hashtags = []
        external_links = []

        try:
            for i in range(10):
                time.sleep(0.1)
                print(range(len(full_text)))
                if all_text:
                    text = all_text[i].text            
                    tweet_text += text
                if hashtag:
                    text = hashtag[i].text 
                    hashtags.append(text)          
                    tweet_text += text
                if mention:
                    text = mention[i].text 
                    mentions.append(text)             
                    tweet_text += text
                if external_link:
                    text = external_link[i].text 
                    external_links.append(text)             
                    tweet_text += text
            print(tweet_text)
        except:
            pass
        # try:
        #     comment1 = dom.xpath('.//div[@data-testid="tweetText"]/span')[0].text
        #     print(comment1)
        # except:
        #     comment1 = ''
        #     pass
        # try: 
        #     comment2 = dom.xpath('.//div[@data-testid="tweetText"]/div/span')[0].text
        #     # print(comment2)
        # except:
        #     comment2 = ''
        #     # print(type(comment2))
        #     pass
        # try:
        #     comment3 = dom.xpath('.//div[@data-testid="tweetText"]/span[2]')[0].text
        #     # print(comment3)
        # except:
        #     comment3 = ''
        #     # print(type(comment3))
        #     pass
        # # time.sleep(0.5)
        # if comment1 == None:
        #     comment1 = ''
        # if comment2 == None:
        #     comment2 == ''
        # if comment3 == None:
        #     comment3 = ''
        # tweet_text = str(comment1) + str(comment2) + str(comment3)
        # print(tweet_text)
        # tweet_text = full_text.text
        # print(tweet_text)
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
        try:
            reply_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[0].text
            print(reply_count)
        except:
            reply_count = ''
        try:
            retweet_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[1].text
            print(retweet_count)
        except:
            retweet_count = ''
        try:
            likes_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[2].text
            print(likes_count)
        except:
            likes_count = ''
        try:
            views_count = dom.xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-qvutc0"]/span')[3].text
            print(views_count)
        except:
            views_count = ''
        # tweets.append(tweet_text)
    except:
        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid = "app-bar-close"]'))).click()
    tweet = (fullname, username, tweet_id, str(tweet_link), str(conversation_id), post_date, tweet_text, json.dumps(list(image_link)), json.dumps(list(hashtags)), json.dumps(list(mentions)), json.dumps(list(external_links)), reply_count, retweet_count, likes_count, views_count)
    return tweet
          



# Scrapes user timeline with it's corresponding reply using twint
# def tweet_scrapper(username, csv_file1):
#     '''
#     :param username: The username of the account from which the tweet will be scraped.
#     :param csv_file1: The file in which all scraped tweets and their replies are saved.

#     This function takes the username and the csv_file1 arguments and feed them to twints config format to scrape the timeline of the given username and replies to a given username before saving it to csv_file1.
#     '''
#     # Configuration for tweets
#     c = twint.Config()
#     c.Username = username
#     c.Store_csv = True
#     #c.Since = since
#     c.Resume = 'tweet.raw'
#     #c.Until = until
#     c.Output = csv_file1
#     c.Count = True
#     # c.Proxy_host = "tor"
#     c.Limit = 200
#     #c.Search = Keyword
#     #c.Verified = True 
#     # twint.run.Search(c)

#     # Run
#     # Set iteration number to scrape more data
#     # Log total numbre of scraped tweets in log/INFO.log
#     try:
#         for i in range(int(iteration_number.get('Account_tweet'))):
#             # total_count = 0
#             time.sleep(3)
#             twint.run.Search(c)
#         f1 = open(csv_file1, 'r', encoding='utf-8')
#         row_count = sum(1 for row in f1) - 1
#         print(row_count)
        
 
#             # result=re.findall(r"\d", c.Count)
#             # total_count = ''
#             # for j in result:
#             #     total_count += j
#             #     print('the total count is '+total_count)
#             # total_count = int(total_count)
#             # print(total_count)
#         # message = 'Number of scraped tweets is ' + str(row_count)
#         # info_log(message)
#         os.remove('tweet.raw')

#     # Error handler
#     # Log error in log/ERROR.log
#     except Exception as e:
#         message = str(e)+' Scraping for ' + username + '\'s account has failed '
#         error_log(message)
#         # stylize('Scraping for ' + username + '\'s account has failed ', colored.fg("red"))
#         # stylize(e, colored.fg("grey_46"))
    
#     # Configuration for replies
#     n = twint.Config()
#     n.Search = "@" + username
#     n.Replies = True
#     n.Resume = 'reply.raw'
#     n.Count = True
#     #n.Since = since
#     #n.Until = until
#     n.To = username
#     # n.Limit = 40
#     n.Store_csv = True
#     n.Output = csv_file1

#     # Run
#     # Set iteration number to scrape more data
#     # Log total numbre of scraped tweets in log/INFO.log
#     try:
#         for i in range(int(iteration_number.get('Account_reply'))):
#             # total_count = 0
#             time.sleep(3)
#             twint.run.Search(n)

#             # result=re.findall(r"\d", c.Count)
#             # total_count = ''
#             # for i in result:
#                 # total_count += i
#             # total_count = int(total_count)
#             # print(total_count)
#         # message = 'Number of scraped replies is ' + str(total_count)
#         # info_log(message)
#         os.remove('reply.raw')

#     # Error handler
#     # Log error in log/ERROR.log
#     except Exception as e:
#         message = str(e)+' \nScraping for replies to ' + username + '\'s account has failed '
#         error_log(message)
#         # stylize('Scraping for replies to ' + username + '\'s account has failed ', colored.fg("red"))
#         # stylize(e, colored.fg("grey_46"))


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