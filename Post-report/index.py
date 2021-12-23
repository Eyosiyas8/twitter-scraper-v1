import csv
import json
from elasticsearch import Elasticsearch, helpers
import pandas as pd
from pandas import *
from datetime import date
import sys
import os
sys.path.insert(0, 'C:/Users/User/PycharmProjects/twitterScraper/venv\Scripts/Scraper')

import profile_scraper
import tweet_scraper

tweet_ids = set()
csv_row1 = []
data = []
es = Elasticsearch()
def data_structure():
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2, open(file3, 'r', encoding='utf-8') as f3:
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
                            'hashtags': row3['hashtags']
                        }
                        tweets_id = ''.join(row3['tweet'])
                        csv_row.append(data)
                tweets_id = ''.join(row2['tweet'])
                if tweets_id not in tweet_ids:
                    tweet_ids.add(tweets_id)
                    csv_rows.append({'id':row2['id'], 'conversation_id':row2['conversation_id'], 'username':row2['username'], 'name':row2['name'], 'tweet':row2['tweet'], 'mentions':row2['mentions'], 'photos':row2['photos'], 'replies_count':row2['replies_count'], 'retweets_count':row2['retweets_count'], 'likes_count':row2['likes_count'], 'hashtags':row2['hashtags'], 'replies':csv_row})
                f3.seek(0)
            f2.seek(0)
            csv_row1.append({'Fullname':row1['Fullname'],
            'UserName': row1['UserName'],
            'Description':row1['Description'],
            'Tweets':row1['Tweets'],
            'Number of Followings': row1['Number of Followings'],
            'Number of Followers': row1['Number of Followers'],
            'Joined_date': row1['Joined_date'],
            'tweets': csv_rows})
            print('almost')
    helpers.bulk(es, csv_row1, index="index_of_"+username.lower())

with open("C:/Users/User/PycharmProjects/twitterScraper/venv/Scripts/Authentication/Document.txt","r", encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    for i in range(len(lines)):
        username=lines[i]
        file1 = 'C:/Users/User/PycharmProjects/twitterScraper/venv/Scripts/csv_files/'+username+'.csv'
        file2 = 'C:/Users/User/PycharmProjects/twitterScraper/venv/Scripts/csv_files/parent_tweet_'+username+'.csv'
        file3 = 'C:/Users/User/PycharmProjects/twitterScraper/venv/Scripts/csv_files/reply_to_'+username+'.csv'
        data_structure()

today = date.today()