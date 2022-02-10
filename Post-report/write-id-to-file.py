from pymongo import MongoClient
from login import *

suspiciousIdList = []
usernameList = []
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = client['twitter-data']
collection = db['twitter']

for obj in collection.find({"tweets.sentiment": "low negative"}):
    tweets = obj['tweets']
    for tweet in tweets:
        if tweet['sentiment'] != 'Unremarkable' and tweet['id'] and tweet['id'] not in suspiciousIdList:
            print(tweet)
            suspiciousIdList.append(tweet['id'])
            file = open('twitter-reporting-ids.txt', 'a')
            file.write(tweet['id'])
            file.write('\n')
            file.close()
for obj in collection.find({"tweets.replies.sentiment": "low negative"},
                           {'tweets.replies.id': 1, 'tweets.replies.sentiment': 1, 'tweets.replies.username': 1}):
    tweets = obj['tweets']
    for tweet in tweets:
        replies = tweet['replies']
        for reply in replies:
            if reply['sentiment'] == 'negative':
                print(reply)
                if reply['id'] and reply['id'] not in suspiciousIdList:
                    suspiciousIdList.append(reply['id'])
                    file = open('twitter-reporting-ids.txt', 'a')
                    file.write(reply['id'])
                    file.write('\n')
                    file.close()
login()
