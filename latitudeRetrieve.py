'''
Created on 8 Jul 2013

@author: James McInerney
'''

#authentication parts of code are copied from example at: https://developers.google.com/api-client-library/python/samples/authorized_api_cmd_line_calendar.py

import httplib2
import time
import json
import pickle

import sys

from oauth2client import client
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


client_id = '[paste your client id here]'
client_secret = '[paste your client secret here]'
ROOT = '[path to directory to store data in]'
numBlocks = 100 #will give you 100,000 most recent data points from user history

# The scope URL for read/write access to a user's calendar data
scope='https://www.googleapis.com/auth/latitude.all.best'

# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

def main(argv):
    
  # Create a Storage object. This object holds the credentials that your
  # application needs to authorize access to the user's data. The name of the
  # credentials file is provided. If the file does not exist, it is
  # created. This object can only hold credentials for a single user, so
  # as-written, this script can only handle a single user.
  storage = Storage('credentials.dat')

  # The get() function returns the credentials for the Storage object. If no
  # credentials were found, None is returned.
  credentials = storage.get()

  # If no credentials are found or the credentials are invalid due to
  # expiration, new credentials need to be obtained from the authorization
  # server. The oauth2client.tools.run() function attempts to open an
  # authorization server page in your default web browser. The server
  # asks the user to grant your application access to the user's data.
  # If the user grants access, the run() function returns new credentials.
  # The new credentials are also stored in the supplied Storage object,
  # which updates the credentials.dat file.
  if credentials is None or credentials.invalid:
    credentials = run(flow, storage)

  # Create an httplib2.Http object to handle our HTTP requests, and authorize it
  # using the credentials.authorize() function.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # The apiclient.discovery.build() function returns an instance of an API service
  # object can be used to make API calls. The object is constructed with
  # methods specific to the calendar API. The arguments provided are:
  #   name of the API ('calendar')
  #   version of the API you are using ('v3')
  #   authorized httplib2.Http() object that can be used for API calls
  service = build('latitude', 'v1', http=http) #

  try:
    earliestTs = '9999999999999' #max ts (i.e., start at most recent readings)
    
    #loop until all pages processed:
    history = []
    data = service.location().list(granularity='best', max_time=earliestTs, max_results='1000').execute()
    while len(history)<numBlocks and 'items' in data and len(data['items'])>1:
        history.append(data['items'])
        #retrieve earliest timestamp in this batch, so that we can go back even further in next batch
        print data
        earliestTs = int(history[-1][-1]['timestampMs'])
        print 'earliestTs',earliestTs
        print '%i blocks retrieved, going back as far as %i (time)'%(len(history), earliestTs)
        time.sleep(2)
        data = service.location().list(granularity='best', max_time=earliestTs, max_results='1000').execute()
    history = [item for sublist in history for item in sublist]
    pickle.dump(history, open(ROOT + 'loc_history.p','w'))
    print 'saved %i items'%len(history)
        
  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
