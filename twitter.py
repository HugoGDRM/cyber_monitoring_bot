#!/usr/bin/env python

import json, requests, re
import text_razor

CYBER_KEYWORD = ['tech', 'cyber', 'war', 'politic', 'security', 'privacy', 'exploit', 'data', 'apt', 'ware', 'attack', 'hack', 'crypt', 'threat', 'compute', 'info', 'telecom']

class Data:
    '''
    Data contructor
    
    :param tweet: The json that represent the tweet
    :param user: The json that represent the user
    :param retweets: The json that represent the retweets
    '''
    def __init__(self, tweet, user, retweets):
        self.tweet = tweet
        self.user = user
        self.retweets = retweets

        # Determined afterward
        self.tweet_score = 0
        self.user_score = 0
        self.total_score = 0
        self.topics = []

    '''
    Data printer
    '''
    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
    
    '''
    Data qualitative scorer
    '''
    def compute_score(self):
        # Red flags
        if self.tweet['possibly_sensitive'] == True or self.user['protected'] == True:
            return

        # Is the tweet contains many entities ?
        if 'entities' in self.tweet:
            entities = self.tweet['entities']
            if 'annotations' in entities:
                self.score += len(entities['annotations']) / 2
            if 'urls' in entities:
                self.score += len(entities['urls']) / 2
            if 'hashtags' in entities:
                self.score += len(entities['hashtags']) / 2

        # Context annotations
        if 'context_annotations' in self.tweet:
            context_annotations = self.tweet['context_annotations']
            for ctx in context_annotations:
                for key in CYBER_KEYWORD:
                    if re.search(key, ctx['entity']['name'], re.IGNORECASE):
                        self.score += 1
                        break
        
        # Is the tweet french or english ?
        if 'lang' in self.tweet:
            if self.tweet['lang'] == 'en' or self.tweet['lang'] == 'fr':
                self.score += 3

        # Content + description
        # Apply topic detection on both tweet's content and user's description to eco API requests
        topics = self.analyzer.analyze(self.tweet['text'] + ' ' + self.user['description'])
        for topic in topics:
            if topic.score < text_razor.TOPIC_TRESHOLD:
                break
            # Save topic
            self.topics.append({'topic':topic.label, 'score': topic.score})
            # Compute score
            for key in CYBER_KEYWORD:
                if re.search(key, topic.label, re.IGNORECASE):
                    self.score += 2
                    break

        # Is the user verified ?
        if self.user['verified'] == True:
            self.score += 7

class API:
    '''
    API contructor
    
    :param twitter_token: Twitter's API bearer token
    '''
    def __init__(self, twitter_token):
        self.twitter_token = twitter_token

    '''
    API query
    '''
    def query(self, url, parameters):
        headers = {'Authorization': f'Bearer {self.twitter_token}'}
        resp = requests.request("GET", url, headers=headers, params=parameters)
        if resp.status_code != 200:
           raise Exception(resp.status_code, resp.text)

        return resp.json()

    '''
    API search tweets
    '''
    def search_tweets(self, search, start_time, end_time, max_result):
        url = 'https://api.twitter.com/2/tweets/search/recent'
        parameters = {
            'query': '(-is:retweet -is:reply -is:quote) (' + search.replace(',', ' OR ') + ')',
            'start_time': start_time,
            'end_time': end_time,
            'max_results': max_result,
            'expansions': 'author_id,geo.place_id',
            'tweet.fields': 'author_id,context_annotations,created_at,entities,geo,id,lang,public_metrics,possibly_sensitive,source,text',
            'user.fields': 'created_at,description,id,location,name,protected,public_metrics,username,verified',
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
            'next_token': {}
        }
        
        try:
            return self.query(url, parameters)
        except Exception:
            return None

    '''
    API search retweets
    '''
    def search_retweets(self, tweet_id, max_result):
        url = f'https://api.twitter.com/2/tweets/{tweet_id}/quote_tweets'
        parameters = {
            #'exclude': 'replies',
            'max_results': max_result,
            'expansions': 'author_id,geo.place_id',
            'tweet.fields': 'author_id,context_annotations,created_at,entities,geo,id,lang,public_metrics,possibly_sensitive,source,text',
            'user.fields': 'created_at,description,id,location,name,protected,public_metrics,username,verified',
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
            'next_token': {}
        }
        
        try:
            return self.query(url, parameters)
        except Exception:
            return None
    
    '''
    Data fetcher
    '''
    def fetch_datas(self, search, start_time, end_time, max_result=10):
        tweets = self.search_tweets(search, start_time, end_time, max_result)
        if tweets is None or 'data' not in tweets:
            return None

        there_is_users = 'includes' in tweets and 'users' in tweets['includes']

        datas = []
        for json_tweet in tweets['data']:
            user, retweets = None, None, 

            # Get associated user
            if there_is_users:
                for json_user in tweets['includes']['users']:
                    if json_user['id'] == json_tweet['author_id']:
                        user = json_user

            # Fetch associated retweets
            retweets = self.search_retweets(json_tweet['id'])

            datas.append(Data(json_tweet, user, retweets))
        
        return datas