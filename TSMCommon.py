#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# Sept 28th, 2014
#################################################

import HTMLParser
import csv

def cleanstring(dirtystr):
    return str(HTMLParser.HTMLParser().unescape(dirtystr))

def createsearchablestring(oldstr):
    return oldstr.translate(None, '@#%^&*()<>?:;{}[]-_+=\|')

def getTotalAveragePrice(avgDict):
    totalPrice = 0
    songCount = 0
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