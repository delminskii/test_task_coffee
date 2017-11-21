#!/usr/bin/python
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


if __name__ == '__main__':
    print sys.ARGV

    ACCESS_TOKEN = os.environ.get('GENIUS_ACCESS_TOKEN')

    sample_artist = 'Madonna'
    sample_song = 'girl gone wild'

    API_HOST = 'https://api.genius.com'
    SEARCH_ENDPOINT = '%s/search' % API_HOST
    ARTISTS_ENDPOINT = '%s/artists' % API_HOST

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
        # TODO
        # results_filtered = 
    else:
        # TODO
        pass


    # sample_song = 'Never Gonna Give You Up'

    # headers = {
        # 'Authorization': 'B'
    # }
