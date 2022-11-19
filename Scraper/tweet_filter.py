import random
import csv
import os
import sys
#import welcome
from log import *
# dependancies = os.environ.get('DEPENDANCIES')
# print(dependancies)
# sys.path.insert(1, dependancies)

# Filter the original tweet from the raw_dump file
def filter_username(username, csv_file1, csv_file2):
    '''
    :param username: The username of the account from which the tweet is scraped.
    :param csv_file1: The csv file in which all the row data (the parent and the child tweets (replies)) are stored.
    :param csv_file3: The csv file in which the parent tweets are stored.

    This function reads the row data from csc_file1 to determine if the tweet is parent tweet or child tweet (reply).

    The way to determine if a tweet is a parent tweet or a child tweet (reply) is by checking if the conversation id is the same as the id of a tweet.

    It then saves the data to csv_file3.
    '''
    with open(csv_file1, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        tweet_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'date':row['date'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'external_link':row['quote_url'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if row["id"] == row["conversation_id"] and username.lower() == row['username']:
                tweet_data.append(data)
                
# Storing data intp a separate csv file
    with open(csv_file2, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames={'id', 'conversation_id', 'username', 'name', 'date', 'tweet', 'mentions', 'photos', 'external_link', 'replies_count',
                 'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(tweet_data)
        f.close()

# Check if a reply is a direct reply of a given tweet
def filter_replies(username, csv_file1, csv_file3):
    '''
    :param username: The username of the account from which the tweet is scraped.
    :param csv_file1: The csv file in which all the row data (the parent and the child tweets (replies)) are stored.
    :param csv_file3: The csv file in which the potential replies to the parent tweets are stored.

    The function then matches the replies with their respective parent tweet by checking the existance of the username inside the first 50 caracters of the reply row and saves the selected rows in csv_file3.

    To determine if its a parent tweet or a child tweet (reply), it checks if the conversation id and the id of the tweet is the same.
    '''
    tweet_ids = set()
    with open(csv_file1, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        reply_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'date':row['date'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'external_link':row['quote_url'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if (username in row['reply_to'][1:50] and row["id"] != row["conversation_id"]):
                tweets_id = ''.join(row['tweet'])
                if tweets_id not in tweet_ids:
                    tweet_ids.add(tweets_id)
                    reply_data.append(data)

# Storing data into a separate csv file
    with open(csv_file3, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames={'id', 'conversation_id', 'username', 'name', 'date', 'tweet', 'mentions', 'photos',
                                            'external_link', 'replies_count',
                                            'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(reply_data)
        f.close()
