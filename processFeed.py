from __future__ import print_function
from alchemyapi_python.alchemyapi import AlchemyAPI
import re
import tweepy as tp

def text_and_url(tweet_text):
    #The regex
    url = re.findall(r'(?:http://|www.)[^"\s]+', tweet_text)
    if url:
        url = url[0]
        return url

def fetch_tweets(api, user):
    id = fetch_id(api, user)
    tweets = api.user_timeline(id=id) #First tweet id = 631165968161632256
    return_tweets = []
    lang = []
    for t in tweets:
        tweet = t.text
        return_tweets.append(tweet)
        lang.append(t.lang)
    return return_tweets


def fetch_id(api, user):
    User = api.get_user(user)
    a = User.id_str
    return a


def entity_extraction(demo_text):
    #print(demo_text)
    texts = []
    response = alchemyapi.entities('text', demo_text, {'sentiment': 1})

    #response = alchemyapi.entities('text', 'I am SUperman, I am Batman, I am Spiderman', {'sentiment': 1})
    if response['status'] == 'OK':
        for entity in response['entities']:
            #print(entity['text'])
            texts.append(entity['text'])
        return texts

    else:
        print('Error in entity extraction call: ', response['statusInfo'])
        print(texts)


def keyword_extraction(demo_text):
    #print(demo_text)
    texts = []
    response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})
    try:
        if response['status'] == 'OK':
            for keyword in response['keywords']:
                #print(keyword['text'])
                texts.append(keyword['text'])
            return texts
        else:
            print('Error in keyword extaction call: ', response['statusInfo'])
    except:
        return None


def title_extraction(demo_url):
    texts = []
    response = alchemyapi.title('url', demo_url)
    if response['status'] == 'OK':
        texts.append(response['title'])
        return texts

    else:
        print('Error in title extraction call: ', response['statusInfo'])


def taxonomy(demo_text):
    texts = []
    #print(demo_text)
    response = alchemyapi.taxonomy('text', demo_text)
    if response['status'] == 'OK':
        for category in response['taxonomy']:
            texts.append(category['label'])
        return texts
    else:
        print('Error in taxonomy call: ', response['statusInfo'])


def authenticate():
    consumer_key = 'Enter your consumer key from the Twitter API here'
    consumer_secret = 'Enter your consumer secret from the Twitter API here'
    access_token = 'Enter your accerss token from the Twitter API here'
    access_token_secret = 'Enter your access token secret from the Twitter API here'

    auth = tp.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tp.API(auth)

alchemyapi = AlchemyAPI()
def processFeed(user):
    try:
        api = authenticate()
        #user = raw_input('Enter Twitter handle: ')
        tweets = fetch_tweets(api, user) #A list of tweets
        #print(len(tweets))

        urls = []
        for tweet in tweets:
            url = text_and_url(tweet)
            if url:
                #print(url)
                urls.append(url)

        keywords = []
        for tweet in tweets:
            #key = taxonomy(tweet)
            #keywords.append(key)
            key = keyword_extraction(tweet)
            keywords.append(key)
            key = entity_extraction(tweet)
            keywords.append(key)
            '''
            for url in urls:
                key = title_extraction(url)
                keywords.append(key)
            '''
        print(keywords)
        return keywords
    except Exception as e:
        print(e)
        print("oops")
