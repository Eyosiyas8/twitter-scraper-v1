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
def scrapper(username, csv_file):
    # Configure
    c = twint.Config()
    c.Username = username
    c.Store_csv = True
    #c.Since = since
    c.Resume = 'n.raw'
    #c.Until = until
    c.Resume = 'resume_file.raw'
    c.Output = csv_file
    c.Count = True
    #c.Search = Keyword
    #c.Verified = True 

    # Run
    try:
        for i in range(10):
            time.sleep(1)
            stylize(twint.run.Search(c), colored.fg("green"))
        os.remove('n.raw')
    except Exception as e:
        stylize('Scraping for ' + username + '\'s account has failed ', colored.fg("red"))
        stylize(e, colored.fg("grey_46"))
    
    # Configure
    n = twint.Config()
    n.Search = "@" + username
    n.Replies = True
    n.Resume = 'n.raw'
    n.Count = True
    #n.Since = since
    #n.Until = until
    n.To = username
    n.Store_csv = True
    n.Output = csv_file
    # Run
    try:
        for i in range(10):
            time.sleep(1)
            stylize(twint.run.Search(n), colored.fg("green"))
        os.remove('n.raw')
    except Exception as e:
        stylize('Scraping for replies to ' + username + '\'s account has failed ', colored.fg("red"))
        stylize(e, colored.fg("grey_46"))

# Filter the original tweet from the raw_dump file
def filter_username(username, csv_file, csv_file1):

    with open(csv_file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        tweet_data = []
        for row in reader:
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'date':row['date'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'external_link':row['quote_url'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if row["id"] == row["conversation_id"] and username.lower() == row['username']:
                tweet_data.append(data)
                
# Storing data intp a separate csv file
    with open(csv_file1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames={'id', 'conversation_id', 'username', 'name', 'date', 'tweet', 'mentions', 'photos', 'external_link', 'replies_count',
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
            data = ({'id':row['id'], 'conversation_id':row['conversation_id'], 'username':row['username'], 'name':row['name'], 'date':row['date'], 'tweet':row['tweet'], 'mentions':row['mentions'], 'photos':row['photos'], 'external_link':row['quote_url'], 'replies_count':row['replies_count'], 'retweets_count':row['retweets_count'], 'likes_count':row['likes_count'], 'hashtags':row['hashtags'], 'language':row['language'], 'link':row['link'], 'video':row['video']})
            if (username in row['reply_to'][1:50] and row["id"] != row["conversation_id"]):
                tweets_id = ''.join(row['tweet'])
                if tweets_id not in tweet_ids:
                    tweet_ids.add(tweets_id)
                    reply_data.append(data)

# Storing data intp a separate csv file
    with open(csv_file2, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file,
                                fieldnames={'id', 'conversation_id', 'username', 'name', 'date', 'tweet', 'mentions', 'photos',
                                            'external_link', 'replies_count',
                                            'retweets_count', 'likes_count', 'hashtags', 'language', 'link', 'video'})
        writer.writeheader()
        writer.writerows(reply_data)
        f.close()
