import twint
import random
import  csv
import os
import sys
dependancies = os.environ.get('DEPENDANCIES')
print(dependancies)
sys.path.insert(1, '/home/ubuntu/Desktop/OSINT/Twitter/twitterScraper/Dependancies')
from color import colored
def scrapper(username, csv_file):
    # Configure
    c = twint.Config()
    c.Username = username
    c.Store_csv = True
    c.Since = '2022-02-08'
    c.Output = csv_file

    # Run
    try:
        colored(255, 150, 50, (twint.run.Search(c)))
    except Exception as e:
        print(colored(255, 200, 100, 'Scraping for ' + username + '\'s account has failed '))
        print(colored(255, 100, 100, e))
    
    # Configure
    n = twint.Config()
    n.Search = "@" + username
    n.Since = '2022-02-08'
    n.Replies = True
    n.Store_csv = True
    n.Output = csv_file
    # Run
    try:
        colored(255, 50, 150, (twint.run.Search(n)))
    except Exception as e:
        print(colored(255, 200, 100, '\nScraping for replies to ' + username + ' has failed'))
        print(colored(255, 100, 100, e))

# Filter the original tweet from the raw_dump file
def filter_username(username, csv_file, csv_file1):

    with open(csv_file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        tweet_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if row["id"] == row["conversation_id"] and username.lower() == row['username']:
                tweet_data.append(data)
                
# Storing data intp a separate csv file
    with open(csv_file1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames={'id', 'conversation_id', 'username', 'name', 'tweet', 'mentions', 'photos', 'replies_count',
                 'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(tweet_data)
        f.close()

# Check if a reply is a direct reply of a given tweet
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

# Storing data intp a separate csv file
    with open(csv_file2, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames={'id', 'conversation_id', 'username', 'name', 'tweet', 'mentions', 'photos',
                                            'replies_count',
                                            'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(reply_data)
        f.close()
