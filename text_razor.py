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
        self.score_treshold = 0.85

    '''
    API analyzer
    
    :param text: Text to analyze
    '''
    def analyze(self, text):
        try:
            # Clean HTML
            self.client.set_cleanup_mode('stripTags')
            resp = self.client.analyze(text)
            return resp
        except textrazor.TextRazorAnalysisException:
            return None