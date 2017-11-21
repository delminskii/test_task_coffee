#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import os
import json
from os.path import join as opj
from os.path import exists as ope
from itertools import imap
from itertools import ifilter
from itertools import izip
import requests

reload(sys)
sys.setdefaultencoding('utf8')


def by_search_str(item, search_str):
    lowered = map(str.strip, search_str.split(' '))
    full_title = str(item['result']['full_title']).lower().strip()
    return all(x in full_title for x in lowered)


if __name__ == '__main__':
    # print sys.argv

    ACCESS_TOKEN = os.environ.get('GENIUS_ACCESS_TOKEN')

    sample_artist = 'Madonna'
    sample_song = 'girl gone wild'

    API_HOST = 'https://api.genius.com'
    HOST = 'https://genius.com'
    SEARCH_ENDPOINT = '%s/search' % API_HOST
    SONGS_ENDPOINT = '%s/songs' % API_HOST

    # make sure we have everything needed making requests to genius.com
    required = (ACCESS_TOKEN, )
    if any(x is None for x in required):
        messages = list()
        if ACCESS_TOKEN is None:
            messages.append('Something\'s wring with Client Access Token')

        print '\n'.join(messages)
        sys.exit(1)

    # special oauth2 header with `Bearer`, see documentation
    headers = {
        'Authorization': 'Bearer %s' % ACCESS_TOKEN
    }

    # params for get request
    params = {
        'q': 'madonna girl gone wild'
    }

    response = requests.get(SEARCH_ENDPOINT, headers=headers, params=params)
    if response.ok:
        json_response = response.json()

        # there're multiple search results sent be their server, so
        # we have to filter them and to look for interesting one for us
        search_results = json_response['response']['hits']
        results_filtered = filter(lambda x: by_search_str(x, params['q']),
                                  search_results)
        if results_filtered:
            # item = results_filtered[0]
            # kw = {
                # 'endpoint': SONGS_ENDPOINT,
                # 'song_id': item['result']['id']
            # }
            # response = requests.get('{endpoint}/{song_id}'.format(**kw),
                                    # headers=headers,
                                    # params={'text_format': 'plain'})
            # if response.ok:
            path = results_filtered[0]['result']['path']
            url = '{host}{path}'.format(host=HOST, path=path)
            print url
        else:
            # TODO
            print 'NOT FOUND'
            pass
    else:
        # TODO
        pass


    # sample_song = 'Never Gonna Give You Up'

    # headers = {
        # 'Authorization': 'B'
    # }
