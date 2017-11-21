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
    ACCESS_TOKEN = os.environ.get('GENIUS_ACCESS_TOKEN')
    ENDPOINT = 'https://api.genius.com/search'

    required = (ACCESS_TOKEN, )
    if any(x is None for x in required):
        messages = list()
        if ACCESS_TOKEN is None:
            messages.append('Something\'s wring with Client Access Token')

        print '\n'.join(messages)
        sys.exit(1)

    headers = {
        'Authorization': 'Bearer %s' % ACCESS_TOKEN
    }
    params = {
        'q': 'Never Gonna Give You Up'
    }

    response = requests.get(ENDPOINT, headers=headers, params=params)
    print response.status_code



    # sample_song = 'Never Gonna Give You Up'

    # headers = {
        # 'Authorization': 'B'
    # }
