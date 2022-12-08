#!/usr/bin/env python3

import configparser, json

import text_razor, twitter

if __name__ == '__main__':
    # Load configuration files
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    api = configparser.ConfigParser()
    api.read('api.ini')

    bot = twitter.API(api['twitter']['bearer_token'], api['text_razor']['bearer_token'])
    data = bot.fetch(config['parameters']['search'], config['parameters']['start_time'], 10)
    for d in data:
        print(d)
        print('======================================')
    