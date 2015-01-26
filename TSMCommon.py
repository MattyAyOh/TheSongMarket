#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# Sept 28th, 2014
#################################################

import HTMLParser
import csv
import urllib2
import datetime
import sys
import os
from TSMApiRequest import tsmApiRequest
dir = os.path.dirname(__file__)

def cleanstring(dirtystr):
    return str(HTMLParser.HTMLParser().unescape(dirtystr))

def createsearchablestring(oldstr):
    return oldstr.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')

def getDateUtilFromString(dateString):
    dateUtil = datetime.datetime.strptime( dateString[:-5], "%Y-%m-%dT%H:%M:%S" )
    return dateUtil

def checkTrackIDExists(TSMTrackID):
    try:
        song_req = tsmApiRequest('/v1/songs/lookup?spotify_uri='+str(TSMTrackID))
    except:
        return False
    return True

def requestResponse(url, length=0):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    if(length == 0):
        return response.read()
    else:
        return response.read(length)

def getTotalAveragePrice():
    totalPrice = 0
    songCount = 0
    avgDict = getAverageDictionary()
    for avgKey, avgValue in avgDict.iteritems():
        totalPrice += int(avgValue)
        songCount += 1
    return totalPrice/songCount

def getAverageDictionary():
    tempDict = {}
    for key, val in csv.reader(open(os.path.join(dir, "averages.csv"))):
        tempDict[key] = val
    return tempDict

def getLastPricesDictionary():
    tempDict = {}
    for key, val in csv.reader(open(os.path.join(dir, "lastPrices.csv"))):
        tempDict[key] = val
    return tempDict

def getLastVCDictionary():
    tempDict = {}
    for key, val in csv.reader(open(os.path.join(dir, "lastVC.csv"))):
        vallist = val.replace('(', '').replace(')','').split(',')
        valtuple = tuple(vallist)
        tempDict[key] = valtuple
    return tempDict

def getTempVCDictionary():
    tempDict = {}
    try:
        for key, val in csv.reader(open(os.path.join(dir, "tempVC.csv"))):
            vallist = val.replace('(', '').replace(')','').split(',')
            valtuple = tuple(vallist)
            tempDict[key] = valtuple
    except IOError:
        tempDict = {}
    return tempDict