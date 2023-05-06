# # import requests
# # from bs4 import BeautifulSoup

# # def scrape_user_timeline(username):
# #     # Define the URL for the user's timeline
# #     url = f'https://twitter.com/{username}'

# #     # Send an HTTP GET request to the URL
# #     response = requests.get(url)

# #     # Check if the response status code is 200 (OK)
# #     if response.status_code == 200:
# #         # Parse the HTML content of the page using BeautifulSoup
# #         soup = BeautifulSoup(response.text, 'html.parser')

# #         # Find all the tweet elements on the page
# #         tweet_elements = soup.find_all('div', {"data-testid": "tweet"})
# #         if tweet_elements != []:
# #             print(tweet_elements[0])

# #         # Loop through each tweet element and extract the tweet text
# #         for tweet_element in tweet_elements:
# #             tweet_text = tweet_element.find('div', {'lang': 'en'}).get_text()
# #             print(tweet_text)
# #     else:
# #         print(f'An error occurred. Status code: {response.status_code}')

# # # Replace 'USERNAME' with the Twitter username you want to scrape
# # scrape_user_timeline('TsedaleLemma')


# import csv
# from time import sleep
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import chromedriver_autoinstaller
# import os

# basedir = os.path.dirname(os.path.abspath(__file__))

# chromedriver_autoinstaller.install()
# options = Options()

# driver = webdriver.Chrome(options=options)

# driver.get('https://www.twitter.com/TsedaleLemma')

# wait = WebDriverWait(driver, 5)
# cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]')))
# print(len(cards))
# tweet_data = []
# for i in range(100):
#     card = cards[i]
#     def get_tweet_data(card):
#         wait = WebDriverWait(driver, 5)
#         fullname = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@data-testid="User-Name"]')))
#         fullname = fullname.text
#         print(fullname)

#         wait = WebDriverWait(driver, 5)
#         username = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "@")]')))
#         username = username.text
#         print(username)
        
#         try:
#             wait = WebDriverWait(driver, 5)
#             post_date = wait.until(EC.presence_of_element_located((By.XPATH, './/time'))).get_attribute('datetime')
#         except:
#             NoSuchElementException
#         print(post_date)

#         wait = WebDriverWait(driver, 5)
#         comment1 = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@data-testid="tweetText"]/span')))
#         comment1 = comment1.text

#         wait = WebDriverWait(driver, 5)
#         comment2 = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@data-testid="tweetText"]/div/span')))
#         comment2 = comment2.text

#         wait = WebDriverWait(driver, 5)
#         comment3 = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@data-testid="tweetText"]/span[2]')))
#         comment3 = comment3.text

#         full_tweet = comment1 + comment2 + comment3
#         print(full_tweet)

#         wait = WebDriverWait(driver, 5)
#         reply_count = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@data-testid="reply"]')))
#         reply_count = reply_count.text
#         print(reply_count)

#         wait = WebDriverWait(driver, 5)
#         retweet_count = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@data-testid="retweet"]')))
#         retweet_count = retweet_count.text
#         print(retweet_count)

#         wait = WebDriverWait(driver, 5)
#         like_count = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@data-testid="like"]')))
#         like_count = like_count.text
#         print(like_count)

#         tweet = {fullname, username, post_date, full_tweet, reply_count, retweet_count, like_count}
#         return tweet

    
#     get_tweet_data(card)
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

#     sleep(2)
#     i+=1 
#     for card in cards:
#         data = get_tweet_data(card)
#         if data:
#             tweet_data.append(data)
# print(tweet_data)


# # try:
# #     wait = WebDriverWait(driver, 5)
# #     element = wait.until(EC.presence_of_element_located((By.XPATH, ("span", {"class": "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}))))
# #     UsernameNotFound = element.text
# #     print(UsernameNotFound)
# #     # error_log('username '+ "username" +' not found!')
# #     pass
# # except:    
# #     try:
# #         wait = WebDriverWait(driver, 5)
# #         element = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(text(), "@")]')))
# #         Fullname = element.text
# #         print("Fullname: " + Fullname)
# #     except:
# #         Fullname = None
# #         print(None)



import requests
from bs4 import BeautifulSoup
from login import *

login()

def scrape_user_timeline(username, csv_timeline):

    try:
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]")))
        element.click()
        time.sleep(1)
    except:
        NoSuchElementException
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@data-testid="SearchBox_Search_Input"]')))
    element.send_keys("@"+username)
    element.send_keys(Keys.ENTER)
    time.sleep(1)

    # Define the URL for the user's timeline
    url = "https://twitter.com/"
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Find all the tweet elements on the page
        tweet_elements = soup.find_all('span')
        print(tweet_elements)

        # Loop through each tweet element and extract the tweet text
        for tweet_element in tweet_elements:
            tweet_text = tweet_element.find('div', {'lang': 'en'}).get_text()
            print(tweet_text)
    else:
        print(f'An error occurred. Status code: {response.status_code}')

# Replace 'USERNAME' with the Twitter username you want to scrape
