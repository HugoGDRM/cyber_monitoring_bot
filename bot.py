#!/usr/bin/env python3

import configparser, json

import text_razor, twitter

if __name__ == '__main__':
    # Load configuration file
    config = configparser.ConfigParser()
    config.read('configuration.ini')

    '''
    bot = twitter.API(config['twitter']['bearer_token'])
    resp = bot.cyber_monitoring(config['twitter']['search'], config['twitter']['start_time'], config['twitter']['max_result'])
    print(json.dumps(resp.json(), indent=4))
     '''
 
    bot = text_razor.API(config['text_razor']['bearer_token'])
    #resp = bot.analyze('It has been a week since the server of #AIIMS was hacked. It raises serious questions about the cybersecurity of the country. In 2020 PM Modi had announced that we will soon have a new Cyber Security Policy. It’s been 2 years and we’re still waiting!')
    resp = bot.analyze("Quelle perspective europ\u00e9enne en mati\u00e8re de cybers\u00e9curit\u00e9 ? L\'urgence d'investir dans l\'expertise humaine - Confrontations Europe")
