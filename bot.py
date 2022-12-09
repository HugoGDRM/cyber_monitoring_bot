#!/usr/bin/env python

import configparser
import text_razor, twitter

if __name__ == '__main__':
    # Load configuration files
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    api = configparser.ConfigParser()
    api.read('api.ini')

    twitter_bot = twitter.API(api['twitter']['bearer_token'])
    text_razor_bot = text_razor.API(api['text_razor']['bearer_token'])

    datas = twitter_bot.fetch_datas(config['parameters']['search'], config['parameters']['start_time'], config['parameters']['end_time'], 10)