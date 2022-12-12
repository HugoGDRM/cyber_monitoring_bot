#!/usr/bin/env python

import configparser
import text_razor, twitter

if __name__ == '__main__':
    # Load config files
    param = configparser.ConfigParser()
    param.read('configuration.ini')
    api = configparser.ConfigParser()
    api.read('api.ini')

    # Bots
    twitter_bot = twitter.API(api['twitter']['bearer_token'])
    text_razor_bot = text_razor.API(api['text_razor']['bearer_token'])

    # Fetch and analyze
    datas = twitter_bot.fetch_datas(param['parameters']['search'], param['parameters']['start_time'],
                                    param['parameters']['end_time'], param['parameters']['max_result'])
    for data in datas:
        data.send()
