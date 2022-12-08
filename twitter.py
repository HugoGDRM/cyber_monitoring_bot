#!/usr/bin/env python3

import json, requests
import text_razor

class Tweet:
    '''
    Tweet contructor.
    
    :param json_obj: The json that represent the tweet.
    '''
    def __init__(self, tweet, user, retweets):
        self.tweet = tweet
        self.user = user
        self.retweets = retweets

    '''
    Tweet printer.
    '''
    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    '''
    Tweet scorer.
    '''
    def get_score(self):
        return


class API:
    def __init__(self, twitter_token, text_razor_token):
        self.headers = {'Authorization': f'Bearer {twitter_token}'}
        self.analyzer = text_razor.API(text_razor_token)

    def query(self, url, parameters):
        resp = requests.request("GET", url, headers=self.headers, params=parameters)
        if resp.status_code != 200:
           raise Exception(resp.status_code, resp.text)
        return resp.json()

    def search_tweets(self, search, start_time, max_result):
        url = 'https://api.twitter.com/2/tweets/search/recent'
        parameters = {
            'query': '(-is:retweet -is:reply -is:quote) (' + search.replace(',', ' OR ') + ')',
            'start_time': start_time,
            'max_results': max_result,
            'expansions': 'author_id,attachments.media_keys,geo.place_id',
            'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,edit_controls,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
            'user.fields': 'created_at,description,id,location,name,protected,public_metrics,username,verified',
            'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics,alt_text,variants',
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
            'next_token': {}
        }
        return self.query(url, parameters)

    def search_retweets(self, tweet_id, max_result=10):
        url = f'https://api.twitter.com/2/tweets/{tweet_id}/quote_tweets'
        parameters = {
            'exclude': 'replies',
            'max_results': max_result,
            'expansions': 'author_id,attachments.media_keys,geo.place_id',
            'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,edit_controls,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
            'user.fields': 'created_at,description,id,location,name,protected,public_metrics,username,verified',
            'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics,alt_text,variants',
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
        }
        return self.query(url, parameters)

    
    def fetch(self, search, start_time, max_result=10):
        resp = self.search_tweets(search, start_time, max_result)

        if 'data' not in resp:
            return None

        there_is_users = 'includes' in resp and 'users' in resp['includes']

        data = []
        for json_tweet in resp['data']:
            user, retweets = None, None, 

            # Get associated user
            if there_is_users:
                for json_user in resp['includes']['users']:
                    if json_user['id'] == json_tweet['author_id']:
                        user = json_user

            # Fetch associated retweets
            retweets = self.search_retweets(json_tweet['author_id'])

            data.append(Tweet(json_tweet, user, retweets))
        
        return data
