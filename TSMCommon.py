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


email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'
apiCREATEURL = 'http://api.thesongmarket.com/v1/songs'

def cleanstring(dirtystr):
    return str(HTMLParser.HTMLParser().unescape(dirtystr))

def createsearchablestring(oldstr):
    return oldstr.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')

def getDateUtilFromString(dateString):
    dateUtil = datetime.datetime.strptime( dateString[:-5], "%Y-%m-%dT%H:%M:%S" )
    return dateUtil

def checkTrackIDExists(TSMTrackID):
    apiCHECKURL = "http://api.thesongmarket.com/v1/songs/"+str(TSMTrackID)+"?user_email="+email+"&user_token="+token
    try:
        request = urllib2.Request(apiCHECKURL)
        urllib2.urlopen(request)
    except urllib2.HTTPError:
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
    for key, val in csv.reader(open("averages.csv")):
        tempDict[key] = val
    return tempDict

def getLastPricesDictionary():
    tempDict = {}
    for key, val in csv.reader(open("lastPrices.csv")):
        tempDict[key] = val
    return tempDict

def getLastVCDictionary():
    tempDict = {}
    for key, val in csv.reader(open("lastVC.csv")):
        vallist = val.replace('(', '').replace(')','').split(',')
        valtuple = tuple(vallist)
        tempDict[key] = valtuple
    return tempDict

def getTempVCDictionary():
    tempDict = {}
    try:
        for key, val in csv.reader(open("tempVC.csv")):
            vallist = val.replace('(', '').replace(')','').split(',')
            valtuple = tuple(vallist)
            tempDict[key] = valtuple
    except IOError:
        tempDict = {}
    return tempDict