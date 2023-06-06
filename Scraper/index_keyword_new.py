from urllib.request import urlopen
from elasticsearch import Elasticsearch, helpers
import urllib3
from keyword_scraper_new import *
# from timeline_tweet_scraper import *
# from tweet_filter import *
from time import sleep
import logging
import tqdm
from pymongo import MongoClient
from datetime import datetime
from log import *
import sys
from sentiment import *

# Initializing mongo db client
db_connection = 'mongodb://localhost:27017/'
db_client = 'twitter-data'
db_collection = 'keyword'
client = MongoClient(db_connection)
print(db_connection)
db = client[db_client]
collection = db[db_collection]

# Initializing different variables
tweet_ids = set()
csv_row1 = []
data = []
es=Elasticsearch([{'host':'localhost:9200','port':9200,'scheme':"http"}])

# Structuring the data generated from the csv files to be inserted to the database

# Initialize the scraping process
acc_name = os.path.join(basedir, '../Authentication/words.txt')
with open(acc_name, "r", encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    keywords = []
    print("current session is {}".format(driver.session_id))

    login()

    for j in sys.argv[1:]:
        keywords.append(j)
    if len(keywords) >= 1:
        for keyword in keywords:
            csv_keyword = os.path.join(basedir, '../csv_files/tweets_') + keyword + '.csv'

            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search query']")))
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            time.sleep(1)
            element.send_keys(keyword)
            element.send_keys(Keys.ENTER)
            time.sleep(3)
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), 'Latest')]")))
            element.click()
            # try:
            # Define the URL for the user's timeline
            # Find all the tweet elements on the page
            data = []
            tweet_ids = set()
            last_position = driver.execute_script('return window.pageYOffset;')
            scrolling = True

            while scrolling:
                # Parse the HTML content of the page using BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'lxml')
                tweet_elements = soup.find_all('article', attrs={'data-testid': 'tweet'})
                print(len(tweet_elements))
                time.sleep(2)
                if len(tweet_elements) == 0:
                    error_log('Keyword isn\'t correct')
                    break
                for tweet_element in tweet_elements:
                    dom = etree.HTML(str(tweet_element))
                    tweet = keyword_scraper(keyword, dom)
                    if tweet:
                        tweet_id = ''.join(tweet)
                        if tweet_id not in tweet_ids:
                            tweet_ids.add(tweet_id)
                            data.append({
                    'username': tweet[0],
                    'name': tweet[1], 'tweet_id': tweet[2], 'tweet_link': tweet[3], 'conversation_id': tweet[4], 'date':tweet[5], 'tweet': tweet[6], 'image_link': tweet[7], 'hashtags': tweet[8], 'mentions': tweet[9], 'link': tweet[10],
                    'replies_count': tweet[11],
                    'retweets_count': tweet[12], 'likes_count': tweet[13], 'views_count': tweet[14],
                    'replies': [], 'reporting': {'is_reported': False, 'reporting_date': None, 'reported_by': None}})
                scroll_attempt = 0
                if len(data) > 50:
                    break
                while True:
                    # check scroll position
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(1)
                    curr_position = driver.execute_script('return window.pageYOffset;')
                    if last_position == curr_position:
                        scroll_attempt=+1

                        # end of scroll region
                        if scroll_attempt >= 3:
                            scrolling = False
                            break
                        else:
                            time.sleep(2) # attempt to scroll again
                    else:
                        last_position = curr_position
                        break

            # except Exception as e:
            #     message = str(e)
            #     error_log(message)
            #     continue
            if data == []:
                pass
            else:
                csv_row1 = []
                csv_row1.append({'Date_of_Scraping': datetime.today(), 'Keyword': keyword, 'tweets': data})
                print(data)
                print('this is csv row one ', csv_row1)
                collection.insert_many(csv_row1)


            # Execute filter_username, filter_replies and data_structure methods
            
            sleep(1)

    else:
        for i in tqdm.tqdm(range(len(lines))):
            print(type(lines))
            print(lines)
            print(type(i))
            sleep(0.1)
            print(lines[i])
            keyword = lines[i]
            print("current session is {}".format(driver.session_id))
            # csv_file = os.path.join(basedir, '../csv_files/') + key_word + ".csv"
            # profile_scraper(keyword, csv_file)
            # print(csv_file)
            csv_keyword = os.path.join(basedir, '../csv_files/tweets_') + keyword + '.csv'
            
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search query']")))
            element.send_keys(keyword)
            element.send_keys(Keys.ENTER)
            time.sleep(3)
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), 'Latest')]")))
            element.click()

            try:
                # Define the URL for the user's timeline
                # Find all the tweet elements on the page
                data = []
                tweet_ids = set()
                last_position = driver.execute_script('return window.pageYOffset;')
                scrolling = True
                x=0
                y=1000
                while scrolling:
                    # Parse the HTML content of the page using BeautifulSoup
                    time.sleep(3)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    tweet_elements = soup.find_all('article', attrs={'data-testid': 'tweet'})
                    time.sleep(3)
                    print(len(tweet_elements))
                    if len(tweet_elements) == 0:
                        error_log('Keyword isn\'t correct')
                        break
                    for tweet_element in tweet_elements:
                        dom = etree.HTML(str(tweet_element))
                        tweet = keyword_scraper(keyword, dom)
                        if tweet[0] == None and tweet[1] == None:
                            continue
                        if tweet:
                            tweet_id = ''.join(tweet)
                            if tweet_id not in tweet_ids:
                                tweet_ids.add(tweet_id)
                                data.append({
                        'username': tweet[0],
                        'name': tweet[1], 'tweet_id': tweet[2], 'tweet_link': tweet[3], 'conversation_id': tweet[4], 'date':tweet[5], 'tweet': tweet[6], 'image_link': tweet[7], 'hashtags': tweet[8], 'mentions': tweet[9], 'link': tweet[10],
                        'replies_count': tweet[11],
                        'retweets_count': tweet[12], 'likes_count': tweet[13], 'views_count': tweet[14],
                        'replies': [], 'reporting': {'is_reported': False, 'reporting_date': None, 'reported_by': None}})
                    scroll_attempt = 0
                    if len(data) < 5:
                        break
                    while True:
                        # check scroll position
                        driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
                        time.sleep(1)
                        x=+1000
                        y+=1000
                        curr_position = driver.execute_script('return window.pageYOffset;')
                        if last_position == curr_position:
                            scroll_attempt+=1

                            # end of scroll region
                            if scroll_attempt >= 3:
                                scrolling = False
                                break
                            else:
                                time.sleep(2) # attempt to scroll again
                        else:
                            last_position = curr_position
                            break
                if data == []:
                    pass
                else:
                    csv_row1 = []
                    csv_row1.append({'Date_of_Scraping': datetime.today(), 'Keyword': keyword, 'tweets': data})
                    print(data)
                    print('this is csv row one ', csv_row1)
                    collection.insert_many(csv_row1)

            except Exception as e:
                message = str(e)
                error_log(message)
                continue
            



            # csv_file1 = os.path.join(basedir, '../csv_files/raw_dump_') + username + ".csv"
            # csv_file2 = os.path.join(basedir, '../csv_files/parent_tweet_') + username + ".csv"
            # csv_file3 = os.path.join(basedir, '../csv_files/reply_of_') + username + ".csv"

            # # Remove raw_dump, parent and reply csv files before scraping if they already exist
            # try:
            #     os.remove(csv_file1)
            #     os.remove(csv_file2)
            #     os.remove(csv_file3)
            
            # Exception handling
            # Logg a warning message to log/WARNING.log
        
            sleep(1)
driver.close()
'''out_file = open("file.json", "w", encoding='utf-8')

json.dump(csv_row1, out_file, indent=6)

out_file.close()'''

sleep(1)
