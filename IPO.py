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

    if(trackExists):
        finalIPOPrice = generateIPO(songURI)
        publishIPO(TSMTrackID, finalIPOPrice)

if __name__ == '__main__':
    listofArgs = sys.argv[1:]
    if len(listofArgs) != 3:
        print "ERROR: Require 3 arguments: TSMTrackID,SpotifyTrackURI,TSMAPIURL"
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

