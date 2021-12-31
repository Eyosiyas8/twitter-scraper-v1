import csv
import json
from elasticsearch import Elasticsearch, helpers

import os

from time import sleep
import tqdm
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = client['twitter-data']
collection = db['twitter']


from profile_scraper import *
from tweet_scraper import *

tweet_ids = set()
csv_row1 = []
data = []
es = Elasticsearch()

def sentiment_output(tweet):
    with open("/home/osint/Desktop/OSINT/Twitter/twitterScraper/Authentication/words.txt", "r",
              encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        count = 0
        sentiment = ''
        for i in range(len(lines)):
            keyWord = lines[i]
            if keyWord in tweet.lower():
                print(keyWord+str(count))
                count += 1
        if count == 1:
            sentiment = 'low negative'
        elif count == 2:
            sentiment = 'negative'
        elif count == 3:
            sentiment = 'very negative'
        elif count >= 4:
            sentiment = 'extremely negative'
        else:
            sentiment = 'Unremarkable'

    return sentiment

def data_structure():
    with open(csv_file, 'r', encoding='utf-8') as f1, open(csv_file2, 'r', encoding='utf-8') as f2, open(csv_file3, 'r', encoding='utf-8') as f3:
        reader1 = csv.DictReader(f1)
        reader2 = csv.DictReader(f2)
        reader3 = csv.DictReader(f3)
        csv_row1 = []
        for row1 in reader1:
            row1['Fullname'] = row1['Fullname']
            row1['UserName'] = row1['UserName']
            row1['Description'] = row1['Description']
            row1['Tweets'] = row1['Tweets']
            row1['Number of Followings'] = row1['Number of Followings']
            row1['Number of Followers'] = row1['Number of Followers']
            row1['Joined_date'] = row1['Joined_date']
            csv_rows = []
            for row2 in reader2:
                row2['id'] = row2['id']
                row2['conversation_id'] = row2['conversation_id']
                row2['username'] = row2['username']
                row2['name'] = row2['name']
                row2['tweet'] = row2['tweet']
                row2['mentions'] = row2['mentions']
                row2['photos'] = row2['photos']
                row2['replies_count'] = row2['replies_count']
                row2['retweets_count'] = row2['retweets_count']
                row2['likes_count'] = row2['likes_count']
                row2['hashtags'] = row2['hashtags']
                csv_row = []
                for row3 in reader3:
                    tweet = row3['tweet']
                    if row2['id'] == row3['conversation_id']:
                        data = {
                            'id': row3['id'],
                            'conversation_id': row3['conversation_id'],
                            'username': row3['username'],
                            'name': row3['name'],
                            'reply': row3['tweet'],
                            'mentions': row3['mentions'],
                            'photos': row3['photos'],
                            'replies_count': row3['replies_count'],
                            'retweets_count': row3['retweets_count'],
                            'likes_count': row3['likes_count'],
                            'hashtags': row3['hashtags'],
                            'sentiment':sentiment_output(tweet)

                        }
                        tweets_id = ''.join(row3['tweet'])
                        csv_row.append(data)
                tweets_id = ''.join(row2['tweet'])
                if tweets_id not in tweet_ids:
                    tweet_ids.add(tweets_id)
                    csv_rows.append(
                        {'sentiment': sentiment_output(tweet),'id': row2['id'], 'conversation_id': row2['conversation_id'], 'username': row2['username'],
                         'name': row2['name'], 'tweet': row2['tweet'], 'mentions': row2['mentions'],
                         'photos': row2['photos'], 'replies_count': row2['replies_count'],
                         'retweets_count': row2['retweets_count'], 'likes_count': row2['likes_count'],
                         'hashtags': row2['hashtags'], 'replies': csv_row})
                f3.seek(0)
            f2.seek(0)
            csv_row1.append({'Fullname': row1['Fullname'],
                             'UserName': row1['UserName'],
                             'Description': row1['Description'],
                             'Tweets': row1['Tweets'],
                             'Number of Followings': row1['Number of Followings'],
                             'Number of Followers': row1['Number of Followers'],
                             'Joined_date': row1['Joined_date'],
                             'tweets': csv_rows})
            print('almost')
    with open(csv_file2, encoding='utf-8') as file1, open(csv_file3, encoding='utf-8') as file2:
        read1 = csv.DictReader(file1)
        read2 = csv.DictReader(file2)
        helpers.bulk(es, read1, index="twitter")
        helpers.bulk(es, read2, index="twitter")
    collection.insert(csv_row1)
    print(csv_row1)

with open("/home/osint/Desktop/OSINT/Twitter/twitterScraper/Authentication/Document.txt","r", encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    for i in tqdm.tqdm(range(len(lines))):
        sleep(1)
        print(((i+1)/(len(lines)))*100, '%')
        username=lines[i]
        url = "https://twitter.com/%s" % username
        print("current session is {}".format(driver.session_id))
        driver.get(url)
        print(url)
        profile_scraper(username)
        csv_file = "/home/osint/Desktop/OSINT/Twitter/twitterScraper/csv_files/" + username + ".csv"
        csv_file1 = "/home/osint/Desktop/OSINT/Twitter/twitterScraper/csv_files/raw_dump_" + username + ".csv"
        csv_file2 = "/home/osint/Desktop/OSINT/Twitter/twitterScraper/csv_files/parent_tweet_" + username + ".csv"
        csv_file3 = "/home/osint/Desktop/OSINT/Twitter/twitterScraper/csv_files/reply_to_" + username + ".csv"
        try:
            os.remove(csv_file1)
            os.remove(csv_file2)
            os.remove(csv_file3)
        except:
            print('No Such File!')
        scrapper(username, csv_file1)
        filter_username(username, csv_file1, csv_file2)
        filter_replies(username, csv_file1, csv_file3)
        sleep(2)
        data_structure()
        sleep(1)
driver.close()
out_file = open("file.json", "w", encoding='utf-8')

json.dump(csv_row1, out_file, indent=6)

out_file.close()

time.sleep(5)