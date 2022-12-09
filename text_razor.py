#!/usr/bin/env python

import textrazor

TOPIC_TRESHOLD = 0.8

class API:
    def __init__(self, bearer_token):
        textrazor.api_key = bearer_token
        self.client = textrazor.TextRazor(extractors=["topics"])

    def analyze(self, text):
        try:
            # Clean HTML
            self.client.set_cleanup_mode('stripTags')
            # Fetch API
            resp = self.client.analyze(text)
        except textrazor.TextRazorAnalysisException:
            return
        return resp.topics()