import twint
import random
import csv
import os
import sys
#import welcome
dependancies = os.environ.get('DEPENDANCIES')
print(dependancies)
sys.path.insert(1, dependancies)
import colored
from colored import stylize

"""
Keyword = input("input the keyword you want to search by: ")
keywordAppend = input("Do you want to append this keyword permanently to the file of you want to use it temporariy? p/t: ")
if keywordAppend == 't':
    print(keywordAppend)
elif keywordAppend == 'p':
    f=open('file.csv', 'a', encoding='utf-8')
    f.write(Keyword)
    print(keywordAppend)
else:
    print("Invalid Entry! Please try again! Thanks for using the scraper! :):)")

since = input("Do you wanna select from when you want to search? y/n: ")
until = input("Do you wanna select until when you want to search? y/n: ")
if until == 'n':
    until = None
    print(until)
elif until == 'y':
    until = input("Enter the date you want to scrape until (use yyyy-mm-dd format): ")
    print(until)
else:
    print("Invalid Entry! Please try again! Thanks for using the scraper! ")

if since == 'n':
    since = None
    print(since)
elif since == 'y':
    since = input("Enter the date you want to scrape since (use yyyy-mm-dd format): ")
    print(since)
else:
    print("Invalid Entry! Please try again! Thanks for using the scraper! ")
"""

def scraper(Keyword, csv_keyword, since, until):
    # Configure
    c = twint.Config()
    #c.Username = username
    c.Store_csv = True
    c.Since = since
    c.Until = until
    c.Output = csv_keyword
    c.Search = Keyword
    #c.Limit = 1
    #c.Verified = True 

    # Run
    try:
        colored(255, 150, 50, (twint.run.Search(c)))
        stylize(twint.run.Search(c), colored.fg("green"))
    except Exception as e:
        stylize('Scraping for ' + Keyword + '\'s account has failed ', colored.fg("red"))
        stylize(e, colored.fg("grey_46"))
        #print(colored(100, e))
    
    # Configure
# Filter the username of the tweet owner

def filter_tweet(Keyword, csv_keyword, username, csv_keyword1):

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
# Scrape replies
def scrape_replies(username, csv_raw_reply):
    n = twint.Config()
    n.Search = "@" + username
    n.Replies = True
    n.Since = "2022-08-04"
    #n.Until = until
    n.To = username
    n.Store_csv = True
    n.Output = csv_raw_reply
    # Run
    try:
        colored(255, 50, 150, (twint.run.Search(n)))
    except Exception as e:
        print(colored(255, 200, 100, '\nScraping for replies to ' + Keyword + ' has failed'))
        print(colored(255, 100, 100, e))

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
