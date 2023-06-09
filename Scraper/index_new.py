from urllib.request import urlopen
from elasticsearch import Elasticsearch, helpers
import urllib3
from timeline_scraper_new import *
# from timeline_tweet_scraper import *
from tweet_filter import *
from time import sleep
import logging
import tqdm
from pymongo import MongoClient
from datetime import datetime
from log import *
import sys
from sentiment import *
from reply_scraper import *

# Initializing mongo db client
db_connection = 'mongodb://localhost:27017/'
db_client = 'twitter-data'
db_collection = 'twitter'
client = MongoClient(db_connection)
print(db_connection)
db = client[db_client]
collection = db[db_collection]

# Initializing different variables
tweet_ids = set()
# csv_row1 = []
es=Elasticsearch([{'host':'localhost:9200','port':9200,'scheme':"http"}])

# Structuring the data generated from the csv files to be inserted to the database

# Initialize the scraping process
acc_name = os.path.join(basedir, '../Authentication/Document.txt')
with open(acc_name, "r", encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    usernames = []
    flag = False

    for j in sys.argv[1:]:
        usernames.append(j)
    if len(usernames) >= 1:
        for username in usernames:
            url = "https://twitter.com/%s" % username
            print("current session is {}".format(driver.session_id))
            driver.get(url)
            print(url)
            csv_file = os.path.join(basedir, '../csv_files/') + username + ".csv"
            profile_info = []
            print(csv_file)
            csv_timeline = os.path.join(basedir, '../csv_files/tweets_') + username + ".csv"
            



            # Define the URL for the user's timeline
            # url = "https://twitter.com/"
            # Send an HTTP GET request to the URL
            # response = requests.get(url)

            # Check if the response status code is 200 (OK)
            try:
                # Find all the tweet elements on the page
                data = []
                tweet_ids = set()
                # last_position = driver.execute_script('return window.pageYOffset;')
                scrolling = True
                x=0
                y=1800
                last_position = driver.execute_script('return window.pageYOffset;')
                while scrolling:
                    # wait = WebDriverWait(driver, 1)
                    # element = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid = "tweet"]')))
                    # print(len(element))
                    
                    # Parse the HTML content of the page using BeautifulSoup
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    tweet_elements = soup.find_all('article', attrs={'data-testid': 'tweet'})
                    print(len(tweet_elements))
                    time.sleep(5)
                    for tweet_element in tweet_elements:
                        dom = etree.HTML(str(tweet_element))
                        tweet = scrape_user_timeline(username, dom)
                        if tweet and tweet[2] != None or tweet[3] != None:
                            tweet_id = ''.join(tweet)
                            if tweet_id not in tweet_ids:
                                tweet_ids.add(tweet_id)
                                tweet_link = tweet[3]
                                tweet_text = tweet[6]
                                # try:
                                #     tweet_data = scrape_replies(username, tweet_link, tweet_text)
                                # except Exception as e:
                                #     print(e)
                                #     error_log(e)
                                if tweet[5] == 'None':
                                    continue
                                else:
                                    data.append({
                        'username': tweet[0],
                        'name': tweet[1], 'tweet_id': tweet[2], 'tweet_link': tweet[3], 'conversation_id': tweet[4], 'date':tweet[5], 'tweet': tweet[6], 'image_link': tweet[7], 'hashtags': tweet[8], 'mentions': tweet[9], 'link': tweet[10],
                        'replies_count': tweet[11],
                        'retweets_count': tweet[12], 'likes_count': tweet[13], 'views_count': tweet[14],
                        'replies': [], 'reporting': {'is_reported': False, 'reporting_date': None, 'reported_by': None}})
                            print(tweet[3])
                            # tweet_link.append(tweet[3])
                            # print(tweet_link)
                        

                    # print(tweet_data)
                    scroll_attempt = 0
                    if len(data) >= 0 and len(data) < 30:
                        pass
                    else:
                        break
                    # while True:
                        # check scroll position
                    print('last position ',last_position)
                    while True:
                        driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
                        time.sleep(1)
                        x+=1000
                        y+=1000
                        curr_position = driver.execute_script('return window.pageYOffset;')
                        print('current position ',curr_position)
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
            except Exception as e:
                print(e)
                error_log(str(e))
                continue        
            url = "https://twitter.com/%s" % username
            driver.get(url)
            profile = profile_scraper(username)
            if profile[0] !=None and profile[1] != None:
                profile_info.append(profile)
                csv_row1 = []
                csv_rows = []
                print(len(data))
                csv_row1.append({
                'Date_of_Scraping': datetime.today(),
                'Fullname': profile[0],
                'UserName': profile[1],
                'Description': profile[2],
                'Tweets': profile[3],
                'Number of Followings': profile[4],
                'Number of Followers': profile[5],
                'Profile_Picture': profile[6],
                'Joined_Date': profile[7],
                'tweets': data})
                print(data)
                print('this is csv row one ', csv_row1)
                collection.insert_many(csv_row1)
            else:
                error_log('Account dosn\'t exist')
                continue

            sleep(1)
            
        
    else:
        for i in tqdm.tqdm(range(len(lines))):
            print(type(lines))
            print(lines)
            print(type(i))
            sleep(0.1)
            print(lines[i])
            username = lines[i]
            url = "https://twitter.com/%s" % username
            print("current session is {}".format(driver.session_id))
            driver.get(url)
            print(url)
            csv_file = os.path.join(basedir, '../csv_files/') + username + ".csv"
            profile_info = []
            print(csv_file)
            csv_timeline = os.path.join(basedir, '../csv_files/tweets_') + username + ".csv"
            



            # Define the URL for the user's timeline
            # url = "https://twitter.com/"
            # Send an HTTP GET request to the URL
            # response = requests.get(url)

            # Check if the response status code is 200 (OK)
            # try:
                # Find all the tweet elements on the page
            data = []
            tweet_ids = set()
            # last_position = driver.execute_script('return window.pageYOffset;')
            scrolling = True
            x=0
            y=1800
            last_position = driver.execute_script('return window.pageYOffset;')
            while scrolling:
                # wait = WebDriverWait(driver, 1)
                # element = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid = "tweet"]')))
                # print(len(element))
                
                # Parse the HTML content of the page using BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                tweet_elements = soup.find_all('article', attrs={'data-testid': 'tweet'})
                print(len(tweet_elements))
                time.sleep(5)
                for tweet_element in tweet_elements:
                    dom = etree.HTML(str(tweet_element))
                    tweet = scrape_user_timeline(username, dom)
                    if tweet and tweet[2] != None or tweet[3] != None:
                        tweet_id = ''.join(tweet)
                        if tweet_id not in tweet_ids:
                            tweet_ids.add(tweet_id)
                            tweet_link = tweet[3]
                            tweet_text = tweet[6]
                            # try:
                            #     tweet_data = scrape_replies(username, tweet_link, tweet_text)
                            # except Exception as e:
                            #     print(e)
                            #     error_log(e)
                            if tweet[5] == 'None':
                                continue
                            else:
                                data.append({
                    'username': tweet[0],
                    'name': tweet[1], 'tweet_id': tweet[2], 'tweet_link': tweet[3], 'conversation_id': tweet[4], 'date':tweet[5], 'tweet': tweet[6], 'image_link': tweet[7], 'hashtags': tweet[8], 'mentions': tweet[9], 'link': tweet[10],
                    'replies_count': tweet[11],
                    'retweets_count': tweet[12], 'likes_count': tweet[13], 'views_count': tweet[14],
                    'replies': [], 'reporting': {'is_reported': False, 'reporting_date': None, 'reported_by': None}})
                        print(tweet[3])
                        # tweet_link.append(tweet[3])
                        # print(tweet_link)
                    

                # print(tweet_data)
                if len(data) >= 0 and len(data) < 30:
                    pass
                else:
                    break
                # while True:
                    # check scroll position
                scroll_atempt = 0
                print('Last position reply ',last_position)
                while True:
                    # try:
                    #     driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
                    # except:
                    #     scrolling = False
                    #     break
                    time.sleep(1)
                    driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
                    x+=1000
                    y+=1000
                    curr_position = driver.execute_script('return window.pageYOffset;')
                    print('current position reply ', curr_position)
                    if last_position == curr_position:
                        print('try scroll again')
                        scroll_atempt+=1
                        print('scroll atempt is ',scroll_atempt)

                        # end of scroll region
                        if scroll_atempt >= 3:
                            print('scroll attempt reached 3 times')
                            scrolling = False
                            break
                        else:
                            time.sleep(2) # attempt to scroll again
                    else:
                        last_position = curr_position
                        print('scrolling again ')
                        break
            # try:
            # scrape_replies(username, data)
            url = "https://twitter.com/%s" % username
            driver.get(url)
            profile = profile_scraper(username)
            if profile[1] !=None and profile[2] != None:
                profile_info.append(profile)
                csv_row1 = []
                csv_rows = []
                print(len(data))
                csv_row1.append({
                'Date_of_Scraping': datetime.today(),
                'Fullname': profile[0],
                'UserName': profile[1],
                'Description': profile[2],
                'Tweets': profile[3],
                'Number of Followings': profile[4],
                'Number of Followers': profile[5],
                'Profile_Picture': profile[6],
                'Joined_Date': profile[7],
                'tweets': data})
                print(data)
                print('this is csv row one ', csv_row1)
                collection.insert_many(csv_row1)
            else:
                error_log('Account dosn\'t exist')
                continue

driver.close()
'''out_file = open("file.json", "w", encoding='utf-8')
json.dump(csv_row1, out_file, indent=6)
out_file.close()'''
