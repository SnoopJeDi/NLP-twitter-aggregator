import requests
import random

baseurl = "http://interest-graph.getprismatic.com"
headers = { 
    'X-API-TOKEN' : "MTQ0NDQ2NzM5MDE5NQ.cHJvZA.amdlcml0eUB0YW11LmVkdQ.Y9smU4pDr0XIglptby2X28A9hB4"
}

def getTopicByName(topicname):
    r = requests.get( baseurl + "/topic/search?&search-query=" + topicname, headers=headers )
    if r.status_code != 200 or len(r.json()['results']) == 0 :
        print( "Ruh roh raggy" )
        print( r.json() )
    return r.json()['results']

def getTopicByText(text):
    r = requests.post( baseurl + "/text/topic", json={ 'body' : text }, headers=headers)
    if r.status_code != 200:
        print( "Ruh roh raggy" )
        print( r.json() )
    return r.json()['topics']

def getTopicByURL(url):
    r = requests.post( baseurl + "/url/topic", json={ 'url' : url }, headers=headers)
    if r.status_code != 200:
        print( "Ruh roh raggy" )
        print( r.json() )
    return r.json()

def getRelatedTopics(topicid):
    r = requests.get( baseurl + "/topic/topic?id=" + topicid, headers=headers)
    if r.status_code != 200:
        print( "Ruh roh raggy" )
        print( r.json() )
    return r.json()['topics']

def getArticlesByTopic(topicid):
    query = { 'topic': topicid }
    r = requests.post( baseurl + "/doc/search" , json={ 'query': { 'topic' : topicid } }, headers=headers )
    retitems = []
    if r.status_code != 200 or len(r.json()['items']) == 0 :
        print( "Ruh roh raggy" )
        print( r.json() )
    for res in r.json()['items'] :
        # no porno, yo
        if not res['aspects']['flag_nsfw']['value']:
            retitems.append( res )
    return retitems
