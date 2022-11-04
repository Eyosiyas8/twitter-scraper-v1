import twint
import random
import csv
import os
import sys
#import welcome
from log import *
# dependancies = os.environ.get('DEPENDANCIES')
# print(dependancies)
# sys.path.insert(1, dependancies)
# import colored
# import time
# from colored import stylize
    
# Filter the username of the tweet owner
def filter_tweet(Keyword, csv_keyword, username, csv_keyword1):
    '''
    :param Keyword: The keyword provided by the user that the scraper uses.
    :param csv_keyword: The file in which all scraped tweets by the given keyword are saved.
    :param username: The username of the account that posted the tweet.
    :param csv_keyword1: The file in which the selected rows are filtered from csv_keyword and saved.

    This function take the above four arguments and filter the rows that are desired and saves them into csv_keyword1.
    '''

    # Filter the original tweet from the raw_dump file
    with open(csv_keyword, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        tweet_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'date':row['date'], 'time':row['time'], 'timezone':row['timezone'], 'username':row['username'], 'name':row['name'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            #print(row['username'])
            if row["id"] == row["conversation_id"] and username.lower() == row['username']:
                tweet_data.append(data)
    
    # Storing data intp a separate csv file
    with open(csv_keyword1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames={'id', 'conversation_id', 'date', 'time', 'timezone', 'username', 'name', 'tweet', 'mentions', 'photos', 'replies_count',
                 'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(tweet_data)
        f.close()
    return csv_keyword1

# Filter the original tweet from the raw_dump file
"""def filter_parent_tweet(username, Keyword, csv_keyword, csv_keyword1):

    with open(csv_file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        tweet_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            tweet_data.append(data)
                
# Storing data intp a separate csv file
    with open(csv_keyword1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames={'id', 'conversation_id', 'username', 'name', 'tweet', 'mentions', 'photos', 'replies_count',
                 'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(tweet_data)
        f.close()
"""

# Check if a reply is a direct reply of a given tweet
def filter_replies(username, csv_raw_reply, csv_reply1): 
    tweet_ids = set()
    with open(csv_raw_reply, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        reply_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if (username in row['reply_to'][1:50] and row["id"] != row["conversation_id"]):
                tweets_id = ''.join(row['tweet'])
                if tweets_id not in tweet_ids:
                    tweet_ids.add(tweets_id)
                    reply_data.append(data)

# Storing data intp a separate csv file
    with open(csv_reply1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames={'id', 'conversation_id', 'username', 'name', 'tweet', 'mentions', 'photos',
                                            'replies_count',
                                            'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(reply_data)
        f.close()
