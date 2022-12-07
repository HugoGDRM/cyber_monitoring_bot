#!/usr/bin/env python3

import json, requests
import text_razor

class User:
    '''
    User contructor.
    
    :param id: The unique identifier of this user.
    :param name: The name of the user.
    :param username: The Twitter screen name.
    :param created_at: The UTC datetime that the user account was created.
    :param description: The text of this user's profile description.
    :param location: The location specified in the user's profile.
    :param protected: Indicates if this user has chosen to protect their Tweets.
    :param verified: Indicates if this user is a verified Twitter User.
    :param followers_count: The number of followers.
    :param following_count: The number of followings.
    :param tweet_count: The number of tweets.
    '''
    def __init__(self, json_obj):
        self.id = json_obj.get('id')
        self.name = json_obj.get('name')
        self.username = json_obj.get('username')
        self.created_at = json_obj.get('created_at')
        self.description = json_obj.get('description')
        self.location = json_obj.get('location')
        self.protected = json_obj.get('protected')
        self.verified = json_obj.get('verified')
        self.followers_count = json_obj.get('public_metrics').get('followers_count')
        self.following_count = json_obj.get('public_metrics').get('following_count')
        self.tweet_count = json_obj.get('public_metrics').get('tweet_count')

    '''
    User printer.
    '''
    def __str__(self):
            return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    '''
    User scorer.
    '''
    def get_score():
        return

class Tweet:
    '''
    Tweet contructor.
    
    :param id: The unique identifier of this user.
    :param text: The actual UTF-8 text of the Tweet.
    :param author_id: The unique identifier of the User who posted this Tweet.
    :param attachments: Specifies the type of attachments
    :param created_at: Creation time of the Tweet.
    :param context_annotations: Contains context annotations for the Tweet.
    :param entities: Entities that have been parsed out of the text of the Tweet.
    :param lang: Language of the Tweet, if detected by Twitter.
    :param possibly_sensitive: This field indicates content may be recognized as sensitive.
    :param retweet_count: The number of retweet.
    :param reply_count: The number of reply.
    :param like_count: The number of like.
    :param quote_count: The number of quote.
    '''
    def __init__(self, json_obj):
        self.id = json_obj.get('id')
        self.text = json_obj.get('text')
        self.author_id = json_obj.get('author_id')
        self.attachments = json_obj.get('attachments')
        self.created_at = json_obj.get('created_at')
        self.context_annotations = json_obj.get('context_annotations')
        self.entities = json_obj.get('entities')
        self.lang = json_obj.get('lang')
        self.possibly_sensitive = json_obj.get('possibly_sensitive')
        self.source = json_obj.get('source')
        self.retweet_count = json_obj.get('public_metrics').get('retweet_count')
        self.reply_count = json_obj.get('public_metrics').get('reply_count')
        self.like_count = json_obj.get('public_metrics').get('like_count')
        self.quote_count = json_obj.get('public_metrics').get('quote_count')

    '''
    Tweet printer.
    '''
    def __str__(self):
            return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    '''
    Tweet scorer.
    '''
    def get_score():
        return

class API:
    def __init__(self, twitter_token, text_razor_token):
        self.headers = {'Authorization': f'Bearer {twitter_token}'}
        self.analyzer = text_razor.API(text_razor_token)

    def fetch(self, url, parameters):
        resp = requests.request("GET", url, headers=self.headers, params=parameters)
        if resp.status_code != 200:
           raise Exception(resp.status_code, resp.text)
        return resp

    def cyber_monitoring(self, search, start_time, max_result=10):
        url = "https://api.twitter.com/2/tweets/search/recent"
        parameters = {
            'query': search.replace(',', ' OR '),
            'start_time': start_time,
            'max_results': max_result,
            'expansions': 'author_id,attachments.media_keys,geo.place_id',
            'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,edit_controls,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
            'user.fields': 'created_at,description,id,location,name,protected,public_metrics,username,verified',
            'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics,alt_text,variants',
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
            'next_token': {}
        }
        
        return self.fetch(url, parameters)