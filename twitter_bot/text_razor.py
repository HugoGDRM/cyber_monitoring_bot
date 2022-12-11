#!/usr/bin/env python

import textrazor

class API:
    '''
    API contructor
    
    :param bearer_token: TAPI bearer token
    '''
    def __init__(self, bearer_token):
        textrazor.api_key = bearer_token
        self.client = textrazor.TextRazor(extractors=["topics"])
        self.score_treshold = 0.5

    '''
    API analyzer
    
    :param text: Text to analyze
    '''
    def analyze(self, text):
        resp = self.client.analyze(text)
        if not resp.ok:
            return None

        json_resp = resp.json
        if 'response' not in json_resp or 'topics' not in json_resp['response']:
            return None
        
        return json_resp['response']['topics']