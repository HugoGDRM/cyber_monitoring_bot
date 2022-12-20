#!/usr/bin/env python

import configparser
import text_razor, twitter
import time
import datetime

def compute_date(date):
    hour = f'0{date.hour}' if date.hour < 10 else f'{date.hour}'
    min = f'0{date.minute}' if date.minute < 10 else f'{date.minute}'
    sec = f'0{date.second}' if date.second < 10 else f'{date.second}'

    return f'{date.year}-{date.month}-{date.day - 2}T{hour}:{min}:{sec}Z'

if __name__ == '__main__':
    # Load config files
    param = configparser.ConfigParser()
    param.read('configuration.ini')
    api = configparser.ConfigParser()
    api.read('api.ini')

    # Compute start_time and end_time
    start = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=30)
    param['parameters']['start_time'] = compute_date(start)

    end = datetime.datetime.now()
    param['parameters']['end_time'] = compute_date(end)

    # Bots
    twitter_bot = twitter.API(api['twitter']['bearer_token'])
    text_razor_bot = text_razor.API(api['text_razor']['bearer_token'])

    # Fetch and analyze
    while (True):
        print("Fetching tweets via Twitter API:")
        datas = twitter_bot.fetch_datas(param['parameters']['search'], param['parameters']['start_time'],
                                        param['parameters']['end_time'], param['parameters']['max_result'])
        if datas != None:
            for data in datas:
                data.compute_score(text_razor_bot)
                print("Sending data to Logstash ...")
                data.send()

        # Wait 30 minutes
        print("Wait for next tweets")
        time.sleep(1800)

        # Modify start_time and end_time
        start = start + datetime.timedelta(hours=0, minutes=30)
        param['parameters']['start_time'] = compute_date(start)
        end = end + datetime.timedelta(hours=0, minutes=30)
        param['parameters']['end_time'] = compute_date(end)

