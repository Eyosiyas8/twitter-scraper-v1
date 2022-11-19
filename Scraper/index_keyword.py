from elasticsearch import Elasticsearch, helpers
from ast import keyword
from pickle import TRUE
from keyword_scraper import *
from keyword_scraper import *
from time import sleep, time
import tqdm
import logging
from pymongo import MongoClient
from datetime import date, timedelta, datetime
# import datetime
import sys
import argparse
from log import *
import csv
from sentiment import *


# Initializing mongo db client
db_connection = os.environ.get('DB_CONNECTION')
db_client = 'twitter-data'
db_collection = 'twitter-keyword'
client = MongoClient(db_connection)
print(db_connection)
db = client[db_client]
collection = db[db_collection]

# Initializing different variables
tweet_ids = set()
csv_row1 = []
data = []
es=Elasticsearch([{'host':'localhost:9200','port':9200,'scheme':"http"}])

# Structuring the data generated from the csv files to be inserted to the database for tweets with no reply
def data_structure_no_reply(csv_keyword, Keyword, since, until):
    '''
    :param csv_keyword: This file contains all tweets scraped from the provided keyword.
    :param keyword: This is the keyword that the tweets are scraped from.
    :param since: This is the starting date of scraping.
    :param until: This is the ending date of scraping.

    This function takes the above arguments before returning a hierarchical structure to be saved in mongoDB.
    '''
    with open(csv_keyword, 'r', encoding='utf-8') as f2:
        reader2 = csv.DictReader(f2)
        # csv_row1 = []
        csv_rows = []
        for row2 in reader2:
            tweet = row2['tweet']
            row2['id'] = row2['id']
            row2['conversation_id'] = row2['conversation_id']
            row2['username'] = row2['username']
            row2['time'] = row2['time']
            row2['date'] = row2['date']
            row2['timezone'] = row2['timezone']
            row2['name'] = row2['name']
            row2['tweet'] = row2['tweet']
            row2['mentions'] = row2['mentions']
            row2['photos'] = row2['photos']
            row2['replies_count'] = row2['replies_count']
            row2['retweets_count'] = row2['retweets_count']
            row2['likes_count'] = row2['likes_count']
            row2['hashtags'] = row2['hashtags']
            # csv_row = []
            # for row3 in reader3:
            #     reply = row3['tweet']
            #     if row2['id'] == row3['conversation_id']:
            #         data = {
            #             'id': row3['id'],
            #             'conversation_id': row3['conversation_id'],
            #             'username': row3['username'],
            #             'name': row3['name'],
            #             'reply': row3['tweet'],
            #             'mentions': row3['mentions'],
            #             'photos': row3['photos'],
            #             'replies_count': row3['replies_count'],
            #             'retweets_count': row3['retweets_count'],
            #             'likes_count': row3['likes_count'],
            #             'hashtags': row3['hashtags'],
            #             'sentiment': sentiment_output(reply)

            #         }
            #         tweets_id = ''.join(row3['tweet'])
            #         csv_row.append(data)
            tweets_id = ''.join(row2['tweet'])
            if tweets_id not in tweet_ids:
                tweet_ids.add(tweets_id)
            csv_rows.append(
                {'sentiment': sentiment_output(tweet), 'id': row2['id'],
                'conversation_id': row2['conversation_id'], 'time': row2['time'], 'date': row2['date'], 'timezone': row2['timezone'],                'timezone':row2['timezone'], 'username': row2['username'],
                'name': row2['name'], 'tweet': row2['tweet'], 'mentions': row2['mentions'],
                'photos': row2['photos'], 'replies_count': row2['replies_count'],
                'retweets_count': row2['retweets_count'], 'likes_count': row2['likes_count'],
                'hashtags': row2['hashtags']})
            #f3.seek(0)
            #f2.seek(0)
        csv_row1.append({'Date_of_Scraping': datetime.today(), 'Keyword': Keyword, 'From_Date': since, 'To_Date': until,'tweets': csv_rows})
            # csv_row1.append({
            #     'Date_of_Scraping': datetime.datetime.today(),
            #     'Fullname': row1['Fullname'],
            #     'UserName': row1['UserName'],
            #     'Description': row1['Description'],
            #     'Tweets': row1['Tweets'],
            #     'Number of Followings': row1['Number of Followings'],
            #     'Number of Followers': row1['Number of Followers'],
            #     'Joined_date': row1['Joined_date'],
            #     'Scraped_From': 'key word',
            #     'Keyword used': Keyword,
            #     'tweets': csv_rows})
            # print('almost')

    # Insert the structured data into a database and an elasticsearch instance
    try:
        with open(csv_keyword, encoding='utf-8') as file1:
            read1 = csv.DictReader(file1)
            helpers.bulk(es, read1, index="twitter_keyword")
        collection.insert_many(csv_row1)
        print(csv_row1)
    
    # Error handling
    # Log an error message to log/ERROR.log
    except Exception as e:
        message = str(e)+" couldn't connect to elasticsearch!"
        error_log(message)
        print(e)
        collection.insert_many(csv_row1)
        print(csv_row1)

# Initialize the scraping process
with open(key_word, "r", encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    Keywords = []
    since = None
    until = None
    for i in sys.argv[1:]:
        if i.count('-')!=2:
            Keywords.append(i)
        elif i.count('-')==2:
            since = i        
            until = sys.argv[(sys.argv.index(since)) + 1]
            # parser = argparse.ArgumentParser()
            # parser.add_argument('date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),)
            # since = parser.parse_args([since]).date
            # until = parser.parse_args([until]).date
            break
    if since is None and until is None:
        until = date.today()
        since = str(until - timedelta(days=7))
        until = str(until)
        #print(since + ', ' + until )
    print(since)
    print(until)
    if len(Keywords) > 0:
        for Keyword in Keywords:
            csv_keyword = os.path.join(basedir, '../csv_files/') + Keyword + '.csv'
            
            # Remove csv_keyword file before scraping if it already exist
            try:
                os.remove(csv_keyword)
                scraper(Keyword, csv_keyword, since, until)
            
            # Jump directly to scraping if csv_keyword doesn't exist
            except:
                scraper(Keyword, csv_keyword, since, until)    
    else:
        for i in tqdm.tqdm(range(len(lines))):
            sleep(0.1)
            Keyword = lines[i]
            csv_keyword = os.path.join(basedir, '../csv_files/') + Keyword + '.csv'
            
            # Remove csv_keyword file before scraping if it already exist
            try:
                os.remove(csv_keyword)
            
            # Exception handling
            # Logg a warning message to log/WARNING.log
            except Exception as e:
                message = str(e)+" No file with the name "+csv_keyword
                warning_log(message)
            scraper(Keyword, csv_keyword, since, until)

    data_structure_no_reply(csv_keyword, Keyword, since, until)
    