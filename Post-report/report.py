import os
from datetime import datetime
from pymongo import MongoClient
suspiciousIdList = []
usernameList = []
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = client['twitter-data']
collection = db['twitter']
results = collection.find({"tweets.replies.sentiment":""})
#print(results)
for obj in collection.find({"tweets.replies.reporting":{'is_reported':True, 'reporting_date':datetime.today(), 'reported_by':'system'}}, {'tweets.replies.id':1, 'tweets.replies.sentiment':1, 'tweets.replies.username':1}):
  tweets = (obj['tweets'])
  for tweet in tweets:
    replies = tweet['replies']
    for reply in replies:
      if reply['sentiment'] == 'negative':
        print(reply)
        suspiciousIdList.append(reply['id'])
        usernameList.append(reply['username'])
        print()