#################################################
# Property of The Song Market
#
# Update csv of average price for an artist
#
# Created by: Matt Ao
# Sept 19th, 2014
#################################################

import HTMLParser
import json
import urllib2
import csv
import createDB
import sqlite3

email = 'mattyayoh@gmail.com'
token = 'PQBTwrEmyRJrR8GMs6ij'

apiGETURL = "http://api.thesongmarket.com/v1/songs?user_email="+email+"&user_token="+token

currentListOfDictOfSongs = []
averagePrice = 0

# Helper Functions:

def cleanstring(dirtystr):
    return str(HTMLParser.HTMLParser().unescape(dirtystr).encode('utf8'))

def createAverages():
    db = sqlite3.connect('records.sqlite')
    c = db.cursor()

    dictionaryTotals = {}
    dictionaryCounts = {}
    dictionaryAverages = {}
    currentListOfDictOfSongs = json.load(urllib2.urlopen(apiGETURL))['results']
    for song in currentListOfDictOfSongs:
        artistName = cleanstring(song['artist_name'])
        if artistName in dictionaryTotals:
            try:
                dictionaryTotals[artistName] += int(song['price'])
            except TypeError:
                dictionaryTotals[artistName] += 10
            dictionaryCounts[artistName] += 1
        else:
            try:
                dictionaryTotals[artistName] = int(song['price'])
            except TypeError:
                dictionaryTotals[artistName] = 10
            dictionaryCounts[artistName] = 1


    for songKey, songValue in dictionaryTotals.items():
        dictionaryAverages[songKey] = int(songValue)/int(dictionaryCounts[songKey])

    w = csv.writer(open("averages.csv", "w+"))
    for key, val in dictionaryAverages.items():
        w.writerow([key, val])

if __name__ == "__main__":
    createDB.check_database()
    createAverages()