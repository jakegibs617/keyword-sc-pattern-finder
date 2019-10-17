#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse
import sys
from googleapiclient import sample_tools

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))


def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')

  request = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['query','page','country'],
      # 'dimensionFilterGroups': [{
          # 'filters': [{
              # 'dimension': 'country',
              # 'operator': 'contains',
              # 'expression': 'gbr'
          # }]
      # }],
      'rowLimit': 100
  }
  response = execute_request(service, flags.property_uri, request)
  print_table(response, 'Top queries and pages')



def execute_request(service, property_uri, request):

  return service.searchanalytics().query(
      siteUrl=property_uri, body=request).execute()


def print_table(response, title):

  # print (response)
  print('\n --' + title + ':')
  
  if 'rows' not in response:
    print('Empty response')
    return

  rows = response['rows']
  row_format = '{:<20}' + '{:>20}' * 6
  print(row_format.format('Keys,', 'Clicks,', 'Impressions,', 'CTR,', 'Position,', 'Page,', 'Country'))
  
  for row in rows:
    keys = ''
    keyword = ''
    key_page = ''
    country = ''
    clicks = ''
    impressions = ''
    ctr = ''
    position = ''
    # Keys are returned only if one or more dimensions are requested.
    if 'keys' in row:
      keys = u','.join(row['keys']).encode('utf-8').decode()
      
      keyword = keys.split(',', 1)[0] + ', '
      
      key_page = (keys.split(',', 1)[1]).split(',', 1)[0] + ', '

      country = (keys.split(',', 1)[1]).split(',', 1)[1] + ', '
      
      clicks = str(row['clicks']) + ', '
      impressions = str(row['impressions']) + ', '
      ctr = str(row['ctr']) + ', '
      position = str(row['position']) + ', '

    print(row_format.format(
        keyword, clicks, impressions, ctr, position, key_page, country))

if __name__ == '__main__':
  main(sys.argv)
