#################################################
# Property of The Song Market
#
# Created by: Matt Ao
# Sept 19th, 2014
#################################################

import HTMLParser
import json
import urllib2
import requests
import csv

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'

apiPOSTURL = 'http://api.thesongmarket.com/v1/songs'
apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token
apiPUTURL = 'http://api.thesongmarket.com/v1/songs'

currentListOfDictOfSongs = []
averagePrice = 0

# Helper Functions:

def cleanstring(dirtystr):
    return str(HTMLParser.HTMLParser().unescape(dirtystr).encode('utf8'))

def createsearchablestring(oldstr):
    return oldstr.translate(None, '!@#%^&*()<>?:;{}[]-_+=\|')

dictionaryTotals = {}
dictionaryCounts = {}
dictionaryAverages = {}
currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
for song in currentListOfDictOfSongs:
    artistName = cleanstring(song['artist_name'])
    if artistName in dictionaryTotals:
        dictionaryTotals[artistName] += int(song['price'])
        dictionaryCounts[artistName] += 1
    else:
        dictionaryTotals[artistName] = int(song['price'])
        dictionaryCounts[artistName] = 1


for songKey, songValue in dictionaryTotals.items():
    dictionaryAverages[songKey] = int(songValue)/int(dictionaryCounts[songKey])

w = csv.writer(open("averages.csv", "w+"))
for key, val in dictionaryAverages.items():
    w.writerow([key, val])