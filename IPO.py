#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# Sept 28th, 2014
#################################################

from TSMSpotify import *
from TSMCommon import *
from IPOCalculate import generateIPO
import requests
import sys
import sqlite3
import os

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'
tsmApiUrl = 'http://api.thesongmarket.com'

dir = os.path.dirname(__file__)

def publishIPO(songID, ipo):
    # market = "Mainstream"
    body = {'user_email': email, 'user_token': token, 'song[ipo_value]': ipo}
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    # print body
    apiUPDATEURL = tsmApiUrl + '/v1/songs/' + str(songID)
    p = requests.put(apiUPDATEURL, data=body, headers=headers)
    print p.status_code
    print p.text

def createIPO(songURI, TSMTrackID=-1):
    #TODO: Check if song is 3 days old on youtube
    trackExists = checkTrackIDExists(TSMTrackID)

    # w = open('logs/ipoLog.txt','a')
    # w.write("\nSong URI: {0}".format(songURI))
    # w.write("\nTrack ID: {0}".format(TSMTrackID))
    # w.write("\nTrack Exists: {0}".format(trackExists))
    # w.close()

    if(trackExists):
        finalIPOPrice = generateIPO(songURI,TSMTrackID)
        publishIPO(TSMTrackID, finalIPOPrice)

if __name__ == '__main__':
    listofArgs = sys.argv[1:]
    for arg in listofArgs:
        print arg
        argsSplit = arg.split(",")
        uri = argsSplit[0]
        id = 0
        try:
            id = int(argsSplit[1])
        except ValueError:
            id = -1
        try:
            tsmApiUrl = argsSplit[2]
        except ValueError:
            pass
        createIPO(uri, id)

