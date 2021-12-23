import twint
import random
from pandas import *
import pandas as pd
import  csv
import codecs
#import os
proxyHost = ['37.59.203.131', '58.234.116.197', '195.158.14.118', '138.68.60.8', '178.18.245.74', '117.20.216.218', '103.149.162.194', '206.253.164.122']
proxyPort = ['1080', '8193', '3128', '8080', '8888', '8080', '80', '80']
def scrapper(username, csv_file):
    # Configure
    rand = random.randrange(0,7)
    c = twint.Config()
    '''c.Proxy_host = proxyHost[rand]
    c.Proxy_port = proxyPort[rand]
    c.Proxy_type = "http"'''
    c.Username = username
    c.Store_csv = True
    c.Output = csv_file
    c.Since = '2021-12-10'

    # Run
    twint.run.Search(c)

    n = twint.Config()
    '''n.Proxy_host = "92.204.251.195"
    n.Proxy_port = "1080"
    n.Proxy_type = "http"'''
    n.Search = "@" + username
    n.Replies = True
    n.Store_csv = True
    n.Output = csv_file
    n.Since = '2021-12-10'
    # Run
    twint.run.Search(n)


def filter_username(username, csv_file, csv_file1):

    with open(csv_file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        tweet_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if row["id"] == row["conversation_id"] and username.lower() == row['username']:
                tweet_data.append(data)

    with open(csv_file1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames={'id', 'conversation_id', 'username', 'name', 'tweet', 'mentions', 'photos', 'replies_count',
                 'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(tweet_data)
        f.close()


def filter_replies(username, csv_file, csv_file2):
    tweet_ids = set()
    with open(csv_file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        reply_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if (username in row['reply_to'][1:50] and row["id"] != row["conversation_id"]):
                tweets_id = ''.join(row['tweet'])
                if tweets_id not in tweet_ids:
                    tweet_ids.add(tweets_id)
                    reply_data.append(data)

    with open(csv_file2, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames={'id', 'conversation_id', 'username', 'name', 'tweet', 'mentions', 'photos',
                                            'replies_count',
                                            'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(reply_data)
        f.close()
