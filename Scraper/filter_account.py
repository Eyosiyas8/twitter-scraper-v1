from urllib.request import urlopen
from elasticsearch import Elasticsearch, helpers
import urllib3
from acc_scraper import *
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

# Initializing mongo db client
db_connection = 'mongodb://localhost:27017/'
db_client = 'twitter-data'
db_collection = 'account_info'
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
acc_name = os.path.join(basedir, '../Authentication/possible_accounts.txt')
with open(acc_name, "r", encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    phrases = []
    print("current session is {}".format(driver.session_id))

    login()
    driver.get('https://twitter.com/explore')

    for j in sys.argv[1:]:
        phrases.append(j)
    if len(phrases) >= 1:
        for phrase in phrases:
            csv_file = os.path.join(basedir, '../csv_files/') + phrase + "_basic_info.csv"

            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search query']")))
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(phrase)
            element.send_keys(Keys.ENTER)
            time.sleep(3)
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), 'People')]")))
            element.click()


            # Define the URL for the user's timeline
            # url = "https://twitter.com/"
            # Send an HTTP GET request to the URL
            # response = requests.get(url)

            # Check if the response status code is 200 (OK)

            # Find all the tweet elements on the page
            try:
                data = []
                tweet_ids = set()
                last_position = driver.execute_script('return window.pageYOffset;')
                scrolling = True
                x=0
                y=800
                while scrolling:
                    # wait = WebDriverWait(driver, 1)
                    # element = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid = "tweet"]')))
                    # print(len(element))
                    
                    # Parse the HTML content of the page using BeautifulSoup
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    acc_elements = soup.find_all('div', attrs={'data-testid': 'cellInnerDiv'})
                    print(len(acc_elements))
                    time.sleep(5)
                    for acc_element in acc_elements[:-1]:
                        dom = etree.HTML(str(acc_element))
                        account_info = acc_info(dom)
                        if account_info and account_info[2] != None or account_info[3] != None:
                            tweet_id = ''.join(account_info)
                            if tweet_id not in tweet_ids:
                                tweet_ids.add(tweet_id)
                                data.append(account_info)
                    scroll_attempt = 0
                    if len(data) >= 0 and len(data) < 5:
                        pass
                    else:
                        break
                    # while True:
                        # check scroll position
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
                if data == []:
                    pass
                else:
                    print('this is account info ', account_info)
                    csv_row1 = []
                    csv_row1.append({'Date_of_Scraping': datetime.today(), 'Search Phrase': phrase, 'Account Info': data})
                    collection.insert_many(csv_row1)
                        # curr_position = driver.execute_script('return window.pageYOffset;')
                        # if last_position == curr_position:
                        #     scroll_attempt=+1

                        #     # end of scroll region
                        #     if scroll_attempt >= 3:
                        #         scrolling = False
                        #         break
                        #     else:
                        #         time.sleep(2) # attempt to scroll again
                        # else:
                        #     last_position = curr_position
                        #     break

            except Exception as e:
                message = str(e)
                error_log(message)
                continue

            # csv_reply= os.path.join(basedir, '../csv_files/replies_') + username + ".csv"
            # scrape_replies(username, csv_reply)



            # csv_file1 = os.path.join(basedir, '../csv_files/raw_dump_') + username + ".csv"
            # csv_file2 = os.path.join(basedir, '../csv_files/parent_tweet_') + username + ".csv"
            # csv_file3 = os.path.join(basedir, '../csv_files/reply_of_') + username + ".csv"

            # Remove raw_dump, parent and reply csv files before scraping if they already exist
            # try:
            #     os.remove(csv_file1)
            #     os.remove(csv_file2)
            #     os.remove(csv_file3)
            
            # Exception handling
            # Logg a warning message to log/WARNING.log
            # except Exception as e:
            #     message = str(e)+' No Such File!'
            #     warning_log(message)
            #     print('No Such File!')
            # # tweet_scrapper(username, csv_file1)

            # Execute filter_username, filter_replies and data_structure methods

            # filter_username(username, csv_file1, csv_timeline)
            # filter_replies(username, csv_file1, csv_file3)
            
            # Exception handling
            # Log error message to log/ERROR.log
            # except Exception as e:
            #     message = str(e)
            #     error_log(message)
            #     # stylize(e, colored.fg("grey_46"))
            #     continue
    else:
        for i in tqdm.tqdm(range(len(lines))):
            print(type(lines))
            print(lines)
            print(type(i))
            sleep(0.1)
            print(lines[i])
            phrase = lines[i]
            csv_file = os.path.join(basedir, '../csv_files/') + phrase + "_basic_info.csv"

            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search query']")))
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(phrase)
            element.send_keys(Keys.ENTER)
            time.sleep(3)
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH, ".//span[contains(text(), 'People')]")))
            element.click()


            # Define the URL for the user's timeline
            # url = "https://twitter.com/"
            # Send an HTTP GET request to the URL
            # response = requests.get(url)

            # Check if the response status code is 200 (OK)

            # Find all the tweet elements on the page
            try:
                data = []
                tweet_ids = set()
                last_position = driver.execute_script('return window.pageYOffset;')
                scrolling = True
                x=0
                y=800
                while scrolling:
                    # wait = WebDriverWait(driver, 1)
                    # element = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid = "tweet"]')))
                    # print(len(element))
                    
                    # Parse the HTML content of the page using BeautifulSoup
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    acc_elements = soup.find_all('div', attrs={'data-testid': 'cellInnerDiv'})
                    print(len(acc_elements))
                    time.sleep(5)
                    for acc_element in acc_elements[:-1]:
                        dom = etree.HTML(str(acc_element))
                        account_info = acc_info(dom)
                        if account_info and account_info[2] != None or account_info[3] != None:
                            tweet_id = ''.join(account_info)
                            if tweet_id not in tweet_ids:
                                tweet_ids.add(tweet_id)
                                data.append(account_info)
                    scroll_attempt = 0
                    if len(data) >= 0 and len(data) < 5:
                        pass
                    else:
                        break
                    # while True:
                        # check scroll position
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
                if data == []:
                    pass
                else:
                    print('this is account info ', account_info)
                    csv_row1 = []
                    csv_row1.append({'Date_of_Scraping': datetime.today(), 'Search Phrase': phrase, 'Account Info': data})
                    collection.insert_many(csv_row1)
                        # curr_position = driver.execute_script('return window.pageYOffset;')
                        # if last_position == curr_position:
                        #     scroll_attempt=+1

                        #     # end of scroll region
                        #     if scroll_attempt >= 3:
                        #         scrolling = False
                        #         break
                        #     else:
                        #         time.sleep(2) # attempt to scroll again
                        # else:
                        #     last_position = curr_position
                        #     break


            except Exception as e:
                message = str(e)
                error_log(message)
                continue

            # csv_reply= os.path.join(basedir, '../csv_files/replies_') + username + ".csv"
            # scrape_replies(username, csv_reply)



            # csv_file1 = os.path.join(basedir, '../csv_files/raw_dump_') + username + ".csv"
            # csv_file2 = os.path.join(basedir, '../csv_files/parent_tweet_') + username + ".csv"
            # csv_file3 = os.path.join(basedir, '../csv_files/reply_of_') + username + ".csv"

            # Remove raw_dump, parent and reply csv files before scraping if they already exist
            # try:
            #     os.remove(csv_file1)
            #     os.remove(csv_file2)
            #     os.remove(csv_file3)
            
            # Exception handling
            # Logg a warning message to log/WARNING.log
            # except Exception as e:
            #     message = str(e)+' No Such File!'
            #     warning_log(message)
            #     print('No Such File!')
            # # tweet_scrapper(username, csv_file1)

            # Execute filter_username, filter_replies and data_structure methods

            # filter_username(username, csv_file1, csv_timeline)
            # filter_replies(username, csv_file1, csv_file3)
            
            # Exception handling
            # Log error message to log/ERROR.log
            # except Exception as e:
            #     message = str(e)
            #     error_log(message)
            #     # stylize(e, colored.fg("grey_46"))
            #     continue
            sleep(1)
driver.close()





