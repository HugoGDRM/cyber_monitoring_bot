#!/usr/bin/env python

import json, re, requests, socket, sys

def is_cyber_related(word):
    CYBER_KEYWORD = ['cyber', 'tech', 'war', 'politic', 'secur', 'privacy', 'exploit', 'data', 'apt', 'ware', 'attack', 'hack', 'crypt', 'threat', 'comput', 'info', 'telecom', 'crime', 'engineer']
    for keyword in CYBER_KEYWORD:
        return re.search(keyword, word, re.IGNORECASE)
    return False

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
        self.score = 0
        self.topics = []

    '''
    Data printer
    '''
    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    '''
    Data qualitative scorer
    '''
    def compute_score(self, text_razor_bot):
        # Red flags
        if self.tweet['possibly_sensitive'] == True or self.user['protected'] == True:
            return

        # Is the tweet french or english ?
        if 'lang' in self.tweet:
            if self.tweet['lang'] == 'en' or self.tweet['lang'] == 'fr':
                self.score += 2

        # Is the tweet contains multiple entities ?
        if 'entities' in self.tweet:
            entities = self.tweet['entities']
            if 'annotations' in entities:
                self.score += 1
            if 'urls' in entities:
                self.score += 1
            if 'hashtags' in entities:
                self.score += 1

        # Context pertinence
        if 'context_annotations' in self.tweet:
            context_annotations = self.tweet['context_annotations']
            for ctx in context_annotations:
                # Check if context is cybersecurity related
                if is_cyber_related(ctx['entity']['name']):
                    self.score += 1

        # Is the user verified ?
        if self.user['verified'] == True:
            self.score += 5

        # Tweet's content and user's description pertinence
        # Apply topic detection on both to eco API requests
        topics = text_razor_bot.analyze(self.tweet['text'])
        if topics is None:
            return

        for topic in topics:
            # Topic recognition confidence
            if topic['score'] < text_razor_bot.score_treshold:
                break

            # Check if topic is cybersecurity related
            if is_cyber_related(topic['label']):
                self.score += 2

            # Save high confidence topics
            self.topics.append(topic)

    def send(self):
        try:
            sock = socket.socket()
        except socket.error as err:
            print('Socket error because of',file=sys.stderr)
        port = 50000
        address = "127.0.0.1"

        try:
            sock.connect((address, port))
            sock.send(json.dumps(self, default=lambda o: o.__dict__, indent=4))
        except socket.gaierror:
            print('There an error resolving the host')

        sys.exit()
        sock.close()

class API:
    '''
    API contructor

    :param bearer_token: API bearer token
    '''
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    '''
    API query

    :param url: URL to query
    :param parameters: Parameters to query
    '''

    def query(self, url, parameters):
        headers = {'Authorization': f'Bearer {self.bearer_token}'}
        resp = requests.request("GET", url, headers=headers, params=parameters)
        if resp.status_code != 200:
           raise Exception(resp.status_code, resp.text)


        return resp.json()

    '''
    API search tweets

    :param keywords: Keywords to search
    :param start_time: Timestamp from where to start searching
    :param end_time: Timestamp to where to stop searching
    :param max_result: Requested maximum number of results
    '''
    def search_tweets(self, keywords, start_time, end_time, max_result):
        url = 'https://api.twitter.com/2/tweets/search/recent'
        parameters = {
            'query': '(-is:retweet -is:reply -is:quote) (' + keywords.replace(',', ' OR ') + ')',
            'start_time': start_time,
            'end_time': end_time,
            'max_results': max_result,
            'expansions': 'author_id,geo.place_id',
            'tweet.fields': 'author_id,context_annotations,created_at,entities,geo,id,lang,public_metrics,possibly_sensitive,source,text',
            'user.fields': 'created_at,description,id,location,name,protected,public_metrics,username,verified',
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
            'next_token': {}
        }

        return self.query(url, parameters)

    '''
    API search retweets

    :param tweet_id: Tweet's identifier
    :param max_result: Requested maximum number of results
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

        return self.query(url, parameters)

    '''
    Data fetcher

    :param keywords: Keywords to search
    :param start_time: Timestamp from where to start searching
    :param end_time: Timestamp to where to stop searching
    :param max_result: Requested maximum number of results
    '''
    def fetch_datas(self, keywords, start_time, end_time, max_result=10):
        tweets = self.search_tweets(keywords, start_time, end_time, max_result)
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
            retweets = self.search_retweets(json_tweet['id'], max_result)

            datas.append(Data(json_tweet, user, retweets))

        return datas
