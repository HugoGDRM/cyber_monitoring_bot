#!/usr/bin/env python3

import textrazor

ENTITY_TRESHOLD = 0.5
TOPIC_TRESHOLD = 0.7

class API:
    def __init__(self, bearer_token):
        textrazor.api_key = bearer_token
        self.client = textrazor.TextRazor(extractors=["entities", "topics"])

    @staticmethod
    def get_related_score(resp):
        print("========ENTITTIES========")
        for e in resp.entities():
            print(e.id, e.relevance_score, e.confidence_score)
        print("========TOPICS========")
        for t in resp.topics():
            if t.score < TOPIC_TRESHOLD:
                break
            print(t.label, t.score)

    def analyze(self, text):
        try:
            # Clean HTML
            self.client.set_cleanup_mode('stripTags')
            # Fetch API
            resp = self.client.analyze(text)
        except textrazor.TextRazorAnalysisException:
            return
        self.get_related_score(resp)