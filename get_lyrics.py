#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import argparse
from time import time as ts
import requests
from bs4 import BeautifulSoup as BS4

reload(sys)
sys.setdefaultencoding('utf8')


def by_search_str(item, search_str):
    """checks if item fits good for search_str string

    :param item: dict-like json object
    :param search_str: string we're searching for
    """
    splitted_chunks = map(str.strip, search_str.split(' '))
    full_title = str(item['result']['full_title']).lower().strip()
    return all(x in full_title for x in splitted_chunks)


def get_lyrics(url, bs4_backend='lxml'):
    """returns lyrics of song located at url

    :param url: string of URL
    :param bs4_backend: backend for beautifulSoup4
    """
    response = requests.get(url)
    if not response.ok:
        print 'Something\'s wrong with %s' % url
        return str()

    # we use lxml instead of default html.parser
    # because it's faster
    soup = BS4(response.text, bs4_backend)
    page_data_tag = soup.select_one('meta[itemprop=page_data]')

    if not page_data_tag:
        print 'Can\'t detect meta tag with itemprop=page_data property'
        return str()

    markup = str()
    try:
        json_value = json.loads(page_data_tag['content'])
        markup = json_value['lyrics_data']['body']['html']
    except KeyError:
        print """
            Something's wrong with `content`, `lyrics_data`, `body`, `html` \
            keys""".strip()
        return str()

    # remove all script tags
    # [s.extract() for s in soup.select('script')]

    return BS4(markup, bs4_backend).text.strip()


def main():
    # read https://docs.genius.com/
    ACCESS_TOKEN = os.environ.get('GENIUS_ACCESS_TOKEN')

    API_HOST = 'https://api.genius.com'
    HOST = 'https://genius.com'
    SEARCH_ENDPOINT = '%s/search' % API_HOST

    # defines mandatory and optional arguments here
    parser = argparse.ArgumentParser(
        description='Script to get lyrics for song from genius.com')
    parser.add_argument('song',
                        type=str.lower,
                        help='Defines a song to search lyrics for')
    parser.add_argument('--output',
                        '-o',
                        default='/tmp/%s_%s.txt' % (__file__, int(ts())),
                        help='Defines an output file to save lyrics on a disk')
    args = parser.parse_args()

    # make sure we have everything needed making requests to genius.com
    required = (ACCESS_TOKEN, )
    if any(x is None for x in required):
        messages = list()
        if ACCESS_TOKEN is None:
            messages.append('Something\'s wrong with Client Access Token')

        # add other checks for `required` tuple here...

        print '\n'.join(messages)
        sys.exit(1)

    # special auth header with `Bearer`, see documentation
    headers = {'Authorization': 'Bearer %s' % ACCESS_TOKEN}

    # params for a GET request
    params = {'q': args.song}

    response = requests.get(SEARCH_ENDPOINT, headers=headers, params=params)
    if response.ok:
        json_response = response.json()

        # there're multiple search results sent by their server, so
        # we have to filter them and to look for interesting one for us
        search_results = json_response['response']['hits']
        results_filtered = filter(lambda x: by_search_str(x, args.song),
                                  search_results)
        if results_filtered:
            path = results_filtered[0]['result']['path']
            url = '{host}{path}'.format(host=HOST, path=path)
            lyrics = get_lyrics(url)
            if lyrics:
                print lyrics
                try:
                    with open(args.output, 'w') as fp:
                        fp.write(lyrics)
                except IOError as e:
                    print 'Can\'t write lyrics to disk at %s' % args.output
                    raise e
        else:
            print 'It semms like song was not found'
    else:
        print 'Can\'t make a search for your song'

if __name__ == '__main__':
    main()
