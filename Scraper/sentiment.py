import os

basedir = os.path.dirname(os.path.abspath(__file__))

# Generates the sentiment for a given tweet
key_word = os.path.join(basedir, '../Authentication/words.txt')
def sentiment_output(tweet):
    '''
    :param tweet: The tweet to bechecked for keywords
    :return sentiment: Implies how many keywords are found in the tweet

    This function reads the tweet column from the csv file and checks if a sentiment keyword is present in the tweet
    '''
    with open(key_word, "r",
              encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        count = 0
        sentiment = ''
        for i in range(len(lines)):
            keyWord = lines[i]
            if keyWord in tweet.lower():
                print(keyWord + str(count))
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